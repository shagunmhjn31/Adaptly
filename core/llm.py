import os, json, re, time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError, ClientError

load_dotenv(override=True)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("MODEL_NAME", "gemini-3.5-flash-lite")
FALLBACK = os.getenv("FALLBACK_MODEL", "")


def _text(response):
    try:
        return response.text or ""
    except Exception:
        return ""


def _generate(contents, config):
    """Main model, then backup. Retries on busy servers and on empty replies."""
    last_err = None
    for model in [m for m in [MODEL, FALLBACK] if m]:
        for attempt in range(3):
            try:
                r = client.models.generate_content(model=model, contents=contents, config=config)
                if _text(r).strip():
                    return r
                last_err = ValueError("The model returned an empty reply.")
                time.sleep(2)
            except ServerError as e:
                last_err = e
                time.sleep(3 * (attempt + 1))
            except ClientError as e:
                last_err = e
                if getattr(e, "code", None) == 429:
                    time.sleep(6 * (attempt + 1))
                else:
                    break
    raise last_err


def ask(prompt: str, system: str = "", max_tokens: int = 2000) -> str:
    r = _generate(prompt, types.GenerateContentConfig(
        system_instruction=system or None, max_output_tokens=max_tokens))
    return _text(r)


def _extract_json(text):
    text = text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    m = re.search(r"(\[.*\]|\{.*\})", text, re.S)
    if not m:
        raise ValueError("No JSON found in the AI reply.")
    return json.loads(m.group(1))


def ask_json(prompt: str, system: str = "", max_tokens: int = 4000):
    system += "\nRespond ONLY with valid JSON. No explanations, no markdown fences."
    last_err = None
    for attempt in range(2):
        r = _generate(prompt, types.GenerateContentConfig(
            system_instruction=system, max_output_tokens=max_tokens + attempt * 4000,
            response_mime_type="application/json"))
        try:
            return _extract_json(_text(r))
        except Exception as e:
            last_err = e
    raise last_err


def _to_contents(history):
    return [types.Content(role="user" if m["role"] == "user" else "model",
                          parts=[types.Part.from_text(text=m["content"])]) for m in history]


def chat(history, system: str = "", max_tokens: int = 4000) -> str:
    r = _generate(_to_contents(history), types.GenerateContentConfig(
        system_instruction=system or None, max_output_tokens=max_tokens))
    return _text(r)


def chat_stream(history, system: str = "", max_tokens: int = 4000):
    """Streams the reply. If streaming fails before any text, falls back to a normal call."""
    contents = _to_contents(history)
    config = types.GenerateContentConfig(system_instruction=system or None,
                                         max_output_tokens=max_tokens)
    for model in [m for m in [MODEL, FALLBACK] if m]:
        started = False
        try:
            for chunk in client.models.generate_content_stream(
                    model=model, contents=contents, config=config):
                if chunk.text:
                    started = True
                    yield chunk.text
            if started:
                return
        except Exception:
            if started:
                raise
    yield _text(_generate(contents, config))