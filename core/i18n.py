import streamlit as st

# key: (English, Hinglish)
STRINGS = {
    # ---------- home ----------
    "tagline": ("Study at your pace, with a plan that adapts to you.",
                "Apni speed se padhein, aisa plan jo aapke hisaab se badalta hai."),
    "welcome": ("Welcome back, {name} 👋", "Wapas swagat hai, {name} 👋"),
    "home_info": ("Language: **{lang}** | Daily study hours: **{hrs}**",
                  "Language: **{lang}** | Roz padhai ke ghante: **{hrs}**"),
    "home_menu": ("Use the sidebar: **Diagnostic** (study style), **Mock Test**, **Study Plan**, "
                  "**AI Helper**, **Check in**, **Dashboard**, **Weak Topic Test**.",
                  "Sidebar use karein: **Diagnostic** (study style), **Mock Test**, **Study Plan**, "
                  "**AI Helper**, **Check in**, **Dashboard**, **Weak Topic Test**."),
    "syl_topics": ("Syllabus topics ({n})", "Syllabus topics ({n})"),
    "acct_created": ("Account created! Found {n} topics. Open Diagnostic from the sidebar.",
                     "Account ban gaya! {n} topics mile. Sidebar se Diagnostic kholein."),

    # ---------- AI helper ----------
    "helper_title": ("🤖 AI Helper", "🤖 AI Sahayak"),
    "helper_caption": ("AI can make mistakes. Verify important things with your textbook or teacher.",
                       "AI galat bhi ho sakta hai. Zaroori baatein kitaab ya teacher se check karein."),
    "mode": ("Mode", "Mode"),
    "mode_doubt": ("💬 Doubt / Explain", "💬 Sawal poochhein"),
    "mode_teach": ("🔁 Teach-back (you explain)", "🔁 Teach-back (aap samjhaayein)"),
    "pick_topic": ("Which topic will you explain?", "Aap kaun sa topic samjhaayenge?"),
    "topic_name": ("Topic name", "Topic ka naam"),
    "teach_info": ("Explain this topic as if teaching a beginner. The AI will act like a curious beginner, "
                   "ask questions and point out gaps.",
                   "Is topic ko aise samjhaiye jaise kisi beginner ko sikha rahe hon. "
                   "AI sawal poochhega aur kamiyan batayega."),
    "btn_feedback": ("📊 Give me feedback", "📊 Feedback dein"),
    "btn_practice": ("📝 Give 5 practice questions", "📝 5 practice sawal dein"),
    "btn_clear": ("🗑️ Clear chat", "🗑️ Chat saaf karein"),
    "chat_input": ("Type your question or explanation...", "Apna sawal ya explanation likhein..."),
    "thinking": ("Thinking...", "Soch raha hun..."),
    "ai_error": ("The AI could not answer. Details below. If it says 503 or 'high demand', wait a minute and try again.",
                 "AI jawab nahi de paya. Neeche details hain. 503 ho to ek minute ruk ke dobara try karein."),
    "feedback_prompt": ("I have finished explaining. Please give feedback on my explanation with a score out of 10.",) * 2,
    "practice_prompt": ("Give 5 practice questions on my weak topics or today's plan topics. "
                        "Give the answers only after I try.",) * 2,

    # ---------- diagnostic ----------
    "diag_title": ("🧠 Study Style Check", "🧠 Study Style Check"),
    "diag_caption": ("Everyday-life situations. There are no right or wrong answers. This only helps us understand "
                     "your study style. It is not a medical or psychological diagnosis.",
                     "Daily life ke situations. Koi sahi ya galat jawab nahi hota. Ye sirf aapka study style "
                     "samajhne ke liye hai, koi medical ya psychological diagnosis nahi."),
    "best_time_q": ("When are you most active in the day?", "Din ka kaun sa time aap sabse active rehte hain?"),
    "submit": ("See my result", "Result dekhein"),
    "answer_all": ("Please answer every question.", "Sabhi sawalon ka jawab dein."),
    "saved": ("Profile saved!", "Profile save ho gayi!"),
    "ai_summary_wait": ("The AI is writing your summary...", "AI aapka summary bana raha hai..."),
    "your_style": ("Your Study Style", "Aapka Study Style"),
    "morning": ("Morning", "Subah"), "afternoon": ("Afternoon", "Dopahar"), "night": ("Night", "Raat"),
    "info_line": ("Best time: **{best}** | Session: **{f} min** study + **{b} min** break | Buffer: **{buf}%**",
                  "Best time: **{best}** | Session: **{f} min** padhai + **{b} min** break | Buffer: **{buf}%**"),

    # ---------- common ----------
    "col_topic": ("Topic", "Topic"), "col_goal": ("Goal", "Goal"), "col_type": ("Type", "Type"),
    "col_correct": ("Correct", "Sahi"), "col_total": ("Total", "Total"), "col_score": ("Score %", "Score %"),
    "type_Exam": ("Exam", "Exam"), "type_Self-study": ("Self-study", "Self-study"),
    "diff_Easy": ("Easy", "Easy"), "diff_Medium": ("Medium", "Medium"), "diff_Hard": ("Hard", "Hard"),
    "general": ("General study", "General padhai"),
    "score_line": ("Score: {c} / {n}", "Score: {c} / {n}"),

    # ---------- mock test ----------
    "mt_title": ("📝 Knowledge Diagnostic & Mock Tests", "📝 Knowledge Diagnostic & Mock Tests"),
    "mt_caption": ("Questions are created from your own syllabus. Results reveal your weak topics, "
                   "and your study plan updates automatically.",
                   "Sawal aapke apne syllabus se bante hain. Result se weak topics pata chalte hain "
                   "aur study plan apne aap update ho jata hai."),
    "mt_extra": ("Extra topics (optional, comma separated), for self-study",
                 "Extra topics (optional, comma se alag), self-study ke liye"),
    "mt_none": ("No syllabus topics found. Add some in the box above.",
                "Syllabus topics nahi mile. Upar wale box mein topics likhein."),
    "mt_type": ("Test type", "Test type"),
    "mt_type_diag": ("Diagnostic (full syllabus)", "Diagnostic (poora syllabus)"),
    "mt_type_topic": ("Topic mock (selected topics)", "Topic mock (chune hue topics)"),
    "mt_n": ("Number of questions", "Kitne sawal"),
    "mt_diff": ("Difficulty", "Difficulty"),
    "mt_choose": ("Choose topics", "Topics chunein"),
    "mt_generate": ("🚀 Generate test", "🚀 Test banayein"),
    "mt_choose_one": ("Choose at least one topic.", "Kam se kam ek topic chunein."),
    "mt_writing": ("The AI is writing your questions (10-30 sec)...", "AI sawal bana raha hai (10-30 sec)..."),
    "mt_error": ("The AI is busy or returned a bad format. Please wait a moment and try once more.",
                 "AI abhi busy hai ya format galat aaya. Thodi der ruk ke ek baar dobara try karein."),
    "mt_submit": ("Submit test", "Test submit karein"),
    "mt_expl": ("Explanations for wrong or skipped questions", "Galat ya chhute sawalon ki explanation"),
    "mt_correct_ans": ("Correct answer", "Sahi jawab"),
    "mt_weak": ("Weak topics (below 60%): ", "Weak topics (60% se kam): "),
    "mt_weak_ok": ("These topics now get extra time on the Study Plan page. Your plan has been updated.",
                   "In topics ko ab Study Plan mein extra time milega. Plan update ho gaya."),
    "mt_noweak": ("No weak topics found. Great work!", "Koi weak topic nahi mila. Badhiya!"),
    "mt_new": ("New test", "Naya test"),

    # ---------- study plan ----------
    "sp_title": ("📅 Goals & Smart Study Plan", "📅 Goals & Smart Study Plan"),
    "sp_new": ("➕ New task (exam or self-study)", "➕ Naya task (exam ya self-study)"),
    "sp_name": ("Subject / goal name (e.g. Maths exam, Learn Python)",
                "Subject / goal ka naam (jaise Maths exam, Learn Python)"),
    "sp_type": ("Type", "Type"),
    "sp_deadline": ("Exam date / target date", "Exam date / target date"),
    "sp_marks": ("Marks / weightage (for self-study, importance 1-100)",
                 "Marks / weightage (self-study mein importance 1-100)"),
    "sp_diff": ("How hard is it for you? (1 easy, 5 hard)", "Aapke liye kitna mushkil hai? (1 easy, 5 hard)"),
    "sp_covered": ("How much of the syllabus is already done (%)?", "Syllabus kitna % ho chuka hai?"),
    "sp_use_syl": ("Use my syllabus topics for this task", "Mere syllabus ke topics is task mein use karein"),
    "sp_topics_text": ("Or type topics (one per line)", "Ya topics likhein (ek line mein ek topic)"),
    "sp_weak": ("Your weak points or difficulties here (optional)", "Isme aapki kamiyan / dikkatein (optional)"),
    "sp_add": ("Add task", "Task add karein"),
    "sp_name_err": ("Please enter a name.", "Naam likhein."),
    "sp_none": ("No tasks yet. Add one above.", "Abhi koi task nahi hai. Upar se add karein."),
    "sp_tasks": ("📋 Your tasks", "📋 Aapke tasks"),
    "sp_task_line": ("**{name}** ({kind}) | {deadline} | {marks:g} marks | difficulty {diff}/5 | "
                     "{cov}% done | {n} topics",
                     "**{name}** ({kind}) | {deadline} | {marks:g} marks | mushkil level {diff}/5 | "
                     "{cov}% complete | {n} topics"),
    "sp_delete": ("Delete", "Delete"),
    "sp_progress": ("📈 Update progress (the plan adjusts to it)", "📈 Progress update karein (plan adjust hota hai)"),
    "sp_save_progress": ("Save progress", "Progress save karein"),
    "sp_plan": ("🗓️ Your plan", "🗓️ Aapka plan"),
    "sp_hours": ("How many hours can you study per day?", "Roz kitne ghante padh sakte hain?"),
    "sp_stressed": ("Your last 3 check-ins showed you were tired or stressed, so the plan is 20% lighter. "
                    "Talking to a teacher, parent or friend can also help.",
                    "Pichhle 3 check-ins mein aap thake ya stressed lage, isliye plan 20% halka kar diya hai. "
                    "Teacher, parent ya dost se baat karna bhi madad karta hai."),
    "sp_examweek": ("🎯 **Exam-week mode ON**: revision-focused plan, lighter sessions and sleep reminders.",
                    "🎯 **Exam-week mode ON**: revision par focus, halke sessions aur neend ka dhyan."),
    "sp_priority": ("Priority topics (weak or missed): ", "Priority topics (weak ya miss hue): "),
    "sp_missed": ("Part of yesterday's plan was missed. No problem, those topics now have priority from today.",
                  "Kal ka kuch plan miss hua, koi baat nahi. Wo topics aaj se priority mein hain."),
    "sp_today": ("✅ Today's plan", "✅ Aaj ka plan"),
    "sp_no_today": ("No tasks today.", "Aaj koi task nahi hai."),
    "sp_today_line": ("**{goal}** - {topic} ({phase}) | {m} min = {s} x {f} min + {b} min break",
                      "**{goal}** - {topic} ({phase}) | {m} min = {s} x {f} min padhai + {b} min break"),
    "sp_save_today": ("Save progress", "Progress save karein"),
    "sp_saved": ("Saved!", "Save ho gaya!"),
    "sp_14": ("📆 Schedule for the next 14 days", "📆 Agle 14 din ka schedule"),
    "col_date": ("Date", "Date"), "col_phase": ("Phase", "Phase"), "col_min": ("Min", "Min"),
    "col_sessions": ("Sessions", "Sessions"), "col_note": ("Note", "Note"),
    "col_days_left": ("Days left", "Bache din"), "col_share": ("Share %", "Share %"),
    "col_hours": ("Hours/day", "Ghante/din"),
    "phase_Learn": ("Learn", "Seekhna"), "phase_Revision": ("Revision", "Revision"),
    "note_exam_week": ("😴 Exam week: sleep 7-8 hours, light revision",
                       "😴 Exam week: 7-8 ghante neend, halka revision"),
    "sp_share": ("⏱️ Today's time share", "⏱️ Aaj ka time share"),
    "sp_advice_h": ("💡 AI advice for your weak points", "💡 Kamiyon ke liye AI advice"),
    "sp_advice_btn": ("Get advice", "Advice dein"),
    "sp_busy": ("{name}: the AI is busy, please try again in a moment.",
                "{name}: AI abhi busy hai, thodi der baad try karein."),

    # ---------- check-in ----------
    "ci_title": ("💚 Daily Check-in", "💚 Daily Check-in"),
    "ci_caption": ("A 30-second check-in. This is not a test or a diagnosis. It only helps keep your plan light or normal.",
                   "30 second ka check-in. Ye koi test ya diagnosis nahi hai, bas plan ko aapke hisaab se "
                   "halka ya normal rakhne ke liye."),
    "mood_1": ("😣 Very stressed", "😣 Bahut tension"), "mood_2": ("😟 A bit stressed", "😟 Thoda stressed"),
    "mood_3": ("😐 Okay", "😐 Theek-thaak"), "mood_4": ("🙂 Good", "🙂 Achha"),
    "mood_5": ("😄 Great", "😄 Bahut achha"),
    "ci_mood_q": ("How are you feeling today?", "Aaj aap kaisa feel kar rahe hain?"),
    "ci_energy": ("Energy level (1 low, 5 high)", "Energy level (1 kam, 5 zyada)"),
    "ci_note": ("Anything to add? (optional)", "Kuch kehna hai? (optional)"),
    "ci_save": ("Save", "Save"),
    "ci_saved": ("Check-in saved.", "Check-in save ho gaya."),
    "ci_low": ("Take it easy today. Keep sessions short, drink water and take breaks. You are not alone.",
               "Aaj thoda halka lein. Chhote sessions rakhein, paani piyein aur break lein. Aap akele nahi hain."),
    "ci_stressed": ("You have seemed tired or stressed for 3 days, so your plan is 20% lighter. "
                    "Please talk to someone you trust (teacher, parent, friend or school counsellor).",
                    "Pichhle 3 din aap thake ya stressed lage, isliye plan 20% halka hai. "
                    "Kisi bharosemand insaan (teacher, parent, dost ya school counsellor) se baat zaroor karein."),
    "ci_help": ("Need help?", "Madad chahiye?"),
    "ci_help_text": ("If the stress is heavy or you feel very low, please talk to someone close to you. "
                     "A free helpline in India: **Tele-MANAS 14416**. Adaptly cannot replace a doctor or counsellor.",
                     "Agar tension bahut zyada ho ya mann bahut bhaari lage, to kisi apne se baat karein. "
                     "India mein free helpline: **Tele-MANAS 14416**. Adaptly doctor ya counsellor ki jagah nahi le sakta."),
    "ci_last14": ("Last 14 days", "Pichhle 14 din"),

    # ---------- dashboard ----------
    "db_title": ("📊 Progress Dashboard", "📊 Progress Dashboard"),
    "db_streak": ("🔥 Streak", "🔥 Streak"),
    "db_days": ("{n} days", "{n} din"),
    "db_total": ("⏱️ Total study", "⏱️ Total padhai"),
    "db_follow": ("✅ Plan followed", "✅ Plan follow"),
    "db_tests": ("📝 Tests", "📝 Tests"),
    "db_scores": ("Test scores (%)", "Test scores (%)"),
    "db_strength": ("Topic-wise strength (%)", "Topic-wise strength (%)"),
    "db_weak": ("Weak topics: ", "Weak topics: "),
    "db_daily": ("Study minutes per day", "Roz ke padhai minutes"),
    "db_mood": ("Mood trend", "Mood trend"),
    "db_nodata": ("No data yet. Take a test, follow your plan and do a check-in, then graphs will appear here.",
                  "Abhi data nahi hai. Ek test dein, plan follow karein aur check-in karein, phir yahan graphs dikhenge."),

    # ---------- weak topic test ----------
    "wt_title": ("🎯 Weak-Topic Aptitude Test", "🎯 Weak-Topic Aptitude Test"),
    "wt_caption": ("This test covers only your weak topics. Difficulty adjusts to your score. "
                   "It is a knowledge check, not a personality or medical test.",
                   "Ye test sirf aapke weak topics par hota hai. Difficulty aapke score ke hisaab se adjust hoti hai. "
                   "Ye knowledge check hai, koi personality ya medical test nahi."),
    "wt_weak_h": ("Your weak topics", "Aapke weak topics"),
    "wt_cur": ("Current score %", "Abhi ka score %"),
    "wt_level": ("Test difficulty", "Test difficulty"),
    "wt_new": ("new / missed", "naya / miss hua"),
    "wt_none": ("No weak topics yet. Take a Diagnostic on the Mock Test page first, or choose topics below.",
                "Abhi koi weak topic nahi hai. Pehle Mock Test page par Diagnostic dein, ya neeche topics chunein."),
    "wt_topics": ("Topics for the test", "Test ke topics"),
    "wt_n": ("Number of questions", "Kitne sawal"),
    "wt_apt": ("Also add logic + numerical aptitude questions", "Logic + numerical aptitude ke sawal bhi jodein"),
    "wt_generate": ("🚀 Generate weak-topic test", "🚀 Weak-topic test banayein"),
    "wt_writing": ("The AI is writing questions for your weak topics (20-40 sec)...",
                   "AI aapke weak topics ke sawal bana raha hai (20-40 sec)..."),
    "wt_error": ("The AI is busy or returned a bad format. Please wait and try once more.",
                 "AI abhi busy hai ya format galat aaya. Thodi der ruk ke ek baar dobara try karein."),
    "wt_before": ("Before %", "Pehle %"), "wt_now": ("This test %", "Is test mein %"),
    "wt_trend": ("Trend", "Trend"),
    "tr_new": ("🆕 First time", "🆕 Pehli baar"), "tr_up": ("📈 Improved", "📈 Sudhar"),
    "tr_same": ("➡️ Same", "➡️ Same"), "tr_down": ("📉 Lower", "📉 Kam"),
    "wt_improved": ("Improved: ", "Sudhar hua: "),
    "wt_still": ("Still weak: ", "Abhi bhi weak: "),
    "wt_still2": (". They now get extra time in your Study Plan.", ". Study Plan mein inko extra time mil gaya hai."),
    "wt_notes_btn": ("📘 Make revision notes for these", "📘 Inke liye revision notes banayein"),
    "wt_notes_wait": ("Writing notes...", "Notes ban rahe hain..."),
    "wt_notes_prompt": ("A student is weak in these topics: {topics}. Write short revision notes for each: "
                        "key ideas, one common mistake and one tiny example. Keep it simple.",) * 2,
    "wt_verify": ("AI can be wrong. Check with your textbook or teacher.",
                  "AI galat bhi ho sakta hai. Textbook ya teacher se check karein."),
    "wt_busy": ("The AI is busy, please try again in a moment.", "AI abhi busy hai, thodi der baad try karein."),
    "wt_all_ok": ("None of these topics are weak any more. Your weak list is updated.",
                  "In topics mein ab koi weak nahi hai. Weak list update ho gayi."),
    "wt_new_btn": ("New weak-topic test", "Naya weak-topic test"),
}


def _idx():
    return 1 if st.session_state.get("language", "English") == "Hindi" else 0


def t(key, **kw):
    pair = STRINGS.get(key)
    if not pair:
        return key
    s = pair[_idx()]
    return s.format(**kw) if kw else s


def lang_rule(language):
    """Tells the AI how to write its reply."""
    if language == "Hindi":
        return ("Reply in Hinglish: Hindi written in Roman (English) letters, NOT Devanagari. "
                "Keep technical terms in English. Use simple everyday words.")
    if language == "Punjabi":
        return ("Reply in Punjabi (Gurmukhi script). Keep technical terms in English. "
                "Use simple everyday words.")
    return "Reply in simple English."