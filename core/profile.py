# Each option: (English, Hinglish, points)
QUESTIONS = [
    {"trait": "structure",
     "q": ("You have a trip in 2 weeks and a work deadline too. What do you do?",
           "2 hafte baad trip pe jana hai aur ek kaam ki deadline bhi hai. Aap kya karte hain?"),
     "options": [("Make a plan right away and work a little every day", "Turant plan banata hun, roz thoda kaam", 3),
                 ("Start after a few days, with a rough plan", "Kuch din baad shuru karta hun, thoda plan ke saath", 2),
                 ("Do everything in the last few days", "Last ke kuch din mein sab ek saath", 1)]},
    {"trait": "structure",
     "q": ("How do you learn a new phone or game?",
           "Koi naya phone ya game seekhna ho to?"),
     "options": [("Read the tutorial or manual first, step by step", "Pehle tutorial/manual padhta hun, step by step", 3),
                 ("Look around a little, then try it myself", "Thoda dekh ke khud try karta hun", 2),
                 ("Start using it and learn from mistakes", "Seedha use karta hun, galti se seekhta hun", 1)]},
    {"trait": "focus",
     "q": ("How does it feel when you work on one task for a long time?",
           "Ek kaam pe lagatar dhyan lagate waqt kaisa lagta hai?"),
     "options": [("My mind wanders after about 30 minutes", "30 minute baad dimaag bhatakne lagta hai", 1),
                 ("I am fine for about 1 hour", "Lagbhag 1 ghanta theek rehta hun", 2),
                 ("I can stay in flow for 2+ hours", "2+ ghante flow mein reh sakta hun", 3)]},
    {"trait": "focus",
     "q": ("You are focused and a phone notification arrives. What do you do?",
           "Focus mein ho aur phone ki notification aaye to?"),
     "options": [("I check it immediately", "Turant dekhta hun", 1),
                 ("I check it a little later", "Thodi der baad dekhta hun", 2),
                 ("I ignore it or keep my phone on silent", "Ignore karta hun ya phone silent rakhta hun", 3)]},
    {"trait": "pressure",
     "q": ("You suddenly find out about a surprise test or presentation. What happens?",
           "Achanak surprise test ya presentation ka pata chale to?"),
     "options": [("I get very anxious and cannot think", "Bahut ghabrahat hoti hai, kuch samajh nahi aata", 1),
                 ("I feel nervous but I prepare", "Nervous hota hun par prepare kar leta hun", 2),
                 ("I see it as a challenge and enjoy it", "Challenge lagta hai, maza aata hai", 3)]},
    {"trait": "pressure",
     "q": ("How do you feel after a mistake or a bad result?",
           "Koi galti ya kharab result aaye uske baad?"),
     "options": [("I stay upset for long and my confidence drops", "Kaafi der tak pareshan rehta hun, confidence gir jata hai", 1),
                 ("I feel bad but recover", "Bura lagta hai par sambhal jata hun", 2),
                 ("I learn from it and move on quickly", "Seekh ke jaldi aage badh jata hun", 3)]},
    {"trait": "drive",
     "q": ("You want to learn a skill with no deadline. What happens?",
           "Bina deadline ke koi skill seekhni ho to?"),
     "options": [("Without a deadline I never start", "Deadline na ho to shuru hi nahi hota", 1),
                 ("I work on it sometimes", "Kabhi kabhi karta hun", 2),
                 ("I practise a little every day on my own", "Roz thoda apne aap karta hun", 3)]},
    {"trait": "drive",
     "q": ("What is your biggest reason to work hard?",
           "Aapko kaam karne ki sabse badi wajah kya hoti hai?"),
     "options": [("Avoiding fear or pressure", "Dar ya pressure se bachna", 1),
                 ("Rewards or praise", "Reward ya tareef", 2),
                 ("Learning and improving myself", "Seekhna aur khud ko behtar banana", 3)]},
    {"trait": "social",
     "q": ("What do you do when you cannot understand something difficult?",
           "Koi mushkil cheez samajh na aaye to?"),
     "options": [("Solve it alone", "Akele khud solve karta hun", 1),
                 ("Try alone first, then ask others", "Pehle khud, phir doosron se poochta hun", 2),
                 ("Discuss with a friend or teacher right away", "Turant dost ya teacher se discuss karta hun", 3)]},
    {"trait": "social",
     "q": ("What kind of place do you like for studying?",
           "Padhai ke liye aapko kaisa mahaul pasand hai?"),
     "options": [("A quiet room, alone", "Shaant, akela kamra", 1),
                 ("Sometimes alone, sometimes in a group", "Kabhi akela, kabhi group", 2),
                 ("Group study with friends", "Dosto ke saath group study", 3)]},
]

TRAIT_LABELS = {
    "structure": ("Planning style", "Planning style"),
    "focus": ("Focus span", "Focus span"),
    "pressure": ("Pressure comfort", "Pressure comfort"),
    "drive": ("Self-drive", "Self-drive"),
    "social": ("Group learning", "Group learning"),
}


def score(points):
    """points: list of 1-3 values, in the same order as QUESTIONS."""
    grouped = {}
    for q, s in zip(QUESTIONS, points):
        grouped.setdefault(q["trait"], []).append(s)
    return {t: round(sum(v) / len(v), 2) for t, v in grouped.items()}


def study_settings(traits):
    f = traits["focus"]
    if f < 1.7:
        focus_min, break_min = 25, 5
    elif f < 2.4:
        focus_min, break_min = 40, 10
    else:
        focus_min, break_min = 55, 10
    buffer_pct = 20 if traits["pressure"] < 1.7 else 10
    return {"focus_min": focus_min, "break_min": break_min, "buffer_pct": buffer_pct}


# (English, Hinglish)
def tips(traits, lang="English"):
    i = 1 if lang == "Hindi" else 0
    t = []
    if traits["structure"] < 1.7:
        t.append(("You work best close to deadlines, so your plan uses small daily targets to keep the last week light.",
                  "Aap deadline ke paas best kaam karte hain, isliye plan mein chhote daily targets rakhenge taaki aakhri hafta bhaari na pade.")[i])
    elif traits["structure"] >= 2.4:
        t.append(("You like planning, so a detailed daily schedule will work well for you.",
                  "Aap planner hain, isliye detailed daily schedule aapke liye achha kaam karega.")[i])
    if traits["focus"] < 1.7:
        t.append(("Short sessions (25 min + 5 min break) suit you best.",
                  "Short sessions (25 min + 5 min break) aapke liye best rahenge.")[i])
    elif traits["focus"] >= 2.4:
        t.append(("You can handle long deep-focus sessions, so hard topics go into those.",
                  "Aap lambe deep-focus sessions kar sakte hain, mushkil topics ko unme rakhenge.")[i])
    if traits["pressure"] < 1.7:
        t.append(("Pressure can feel heavy, so your plan includes extra buffer days and a lighter final week.",
                  "Pressure mein tension ho sakti hai, isliye plan mein extra buffer days aur halka final week rakhenge.")[i])
    if traits["drive"] < 1.7:
        t.append(("Deadlines motivate you, so each topic gets small mini-deadlines.",
                  "Deadline se motivation milti hai, isliye har topic ke liye chhoti mini-deadlines banayenge.")[i])
    if traits["social"] >= 2.4:
        t.append(("Group discussion helps you, so try 1-2 discussion sessions a week.",
                  "Group discussion aapko help karti hai, hafte mein 1-2 discussion sessions rakhein.")[i])
    elif traits["social"] < 1.7:
        t.append(("You study well alone, so choose a quiet place for deep work.",
                  "Aap akele achha padhte hain, deep work ke liye shaant jagah chunein.")[i])
    if not t:
        t.append(("Your style is balanced, so your plan stays flexible.",
                  "Aapka style balanced hai, plan flexible rahega.")[i])
    return t