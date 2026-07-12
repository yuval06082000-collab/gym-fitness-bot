import base64
import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://server.iac.ac.il/api/v1/studentapi/responses"
API_KEY = os.getenv("API_KEY")
TRAINER_NAME = "יובל"
TRAINER_PHONE = "0528775898"
GYM_NAME = "ST-FITNESS"
MAX_MESSAGES = 20

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

SYSTEM_PROMPT = f"""
אתה בן — מאמן הכושר האגדי של {GYM_NAME}. אתה נלהב, כריזמטי, ומלא אנרגיה!

הסגנון שלך:
- תמיד פתח עם מחמאה או עידוד ("וואו, שאלה מעולה!", "כל הכבוד שאתה שואל!", "אני גאה בך!")
- השתמש בהרבה אמוג'י 💪🔥⚡🏆💥
- ענה בעברית, קצר וברור — מקסימום 3 משפטים
- סיים תמיד עם משפט מעודד ("קדימה אלוף!", "אתה מדהים!", "ממשיכים להתקדם!")
- אל תמציא מידע רפואי — הפנה לרופא
- אם רוצים לדבר עם המאמן — אמור ללחוץ על הכפתור למטה
"""


def get_logo_b64():
    if os.path.exists("logo.jpg"):
        with open("logo.jpg", "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


def call_api_smart(messages):
    user_input = messages[-1]["content"] if messages else "היי"

    payload = {
        "reasoning": {"effort": "low"},
        "instructions": SYSTEM_PROMPT,
        "input": user_input
    }

    try:
        r = requests.post(API_URL, json=payload, headers=HEADERS, timeout=90)
        if r.status_code == 200:
            data = r.json()
            bot_reply = data.get("output") or data.get("answer") or data
            if bot_reply:
                return str(bot_reply).strip()
        else:
            return f"❌ שגיאת תקשורת (קוד {r.status_code})"
    except Exception as e:
        return f"❌ שגיאה: {str(e)[:50]}"

    return "🙏 לא הצלחתי לענות, נסה שוב!"


def analyze_image(image_b64, mime, description):
    payload = {
        "reasoning": {"effort": "low"},
        "instructions": f"{SYSTEM_PROMPT} תנתח את התמונה המצורפת מבחינת כושר ותזונה.",
        "input": description or "תנתח את התמונה מבחינת כושר/תזונה בקצרה",
        "image_url": f"data:{mime};base64,{image_b64}"
    }
    try:
        r = requests.post(API_URL, json=payload, headers=HEADERS, timeout=90)
        if r.status_code == 200:
            data = r.json()
            bot_reply = data.get("output") or data.get("answer") or data
            if bot_reply:
                return str(bot_reply).strip()
    except Exception:
        pass
    return "לא הצלחתי לנתח את התמונה, נסה שוב 🙏"


logo_b64 = get_logo_b64()

st.set_page_config(page_title=GYM_NAME, page_icon="💪", layout="centered")

bg = (
    f'background-image: url("data:image/jpeg;base64,{logo_b64}"); '
    'background-size: 50%; background-position: center; '
    'background-repeat: no-repeat; background-attachment: fixed;'
) if logo_b64 else ''

st.markdown(f"""
<style>
    body {{ direction: rtl; }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    .stApp {{ background-color: #111; {bg} }}
    .stApp::before {{
        content: ""; position: fixed; inset: 0;
        background: rgba(0,0,0,0.85); z-index: 0; pointer-events: none;
    }}
    .block-container {{
        position: relative; z-index: 1;
        padding: 0 1rem 5rem 1rem !important; max-width: 100% !important;
    }}
    .wa-header {{
        background: rgba(20,20,20,0.97); color: white; padding: 12px 16px;
        display: flex; align-items: center; gap: 12px;
        margin: -1rem -1rem 1rem -1rem; border-bottom: 3px solid #c0392b; z-index: 10;
    }}
    .wa-name {{ font-weight: bold; font-size: 16px; }}
    .wa-status {{ font-size: 12px; color: #e74c3c; }}
    .chat-wrap {{ background: rgba(236,229,221,0.95); border-radius: 12px; padding: 10px; margin-bottom: 10px; }}
    .msg-user {{
        background: #DCF8C6; padding: 8px 12px; border-radius: 12px 2px 12px 12px;
        margin: 6px 0 6px auto; max-width: 80%; width: fit-content;
        text-align: right; font-size: 14px; line-height: 1.6;
        word-break: break-word; white-space: pre-wrap;
    }}
    .msg-bot {{
        background: white; padding: 8px 12px; border-radius: 2px 12px 12px 12px;
        margin: 6px auto 6px 0; max-width: 80%; width: fit-content;
        text-align: right; font-size: 14px; line-height: 1.6;
        border-right: 3px solid #c0392b; word-break: break-word; white-space: pre-wrap;
    }}
    .msg-time {{ font-size: 11px; color: #999; margin-top: 3px; }}
    .msg-wrapper-user {{ display: flex; justify-content: flex-end; width: 100%; }}
    .msg-wrapper-bot  {{ display: flex; justify-content: flex-start; width: 100%; }}
    .thinking-box {{
        background: white; padding: 10px 16px; margin: 6px auto 6px 0; width: fit-content;
        border-radius: 2px 12px 12px 12px; border-right: 3px solid #c0392b;
        font-weight: bold; color: #c0392b;
    }}
    .stButton > button {{
        background: linear-gradient(135deg, #c0392b, #922b21) !important;
        color: white !important; border: none !important; border-radius: 25px !important;
        padding: 10px 20px !important; font-size: 15px !important; font-weight: bold !important;
        width: 100% !important;
    }}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content":
            f"היי! 👋 ברוך הבא לבוט של {GYM_NAME}! 🔥\n"
            "אני כאן לעזור לך לשבור שיאים 💪⚡\n"
            "שאל אותי הכל — כושר, תזונה, מוטיבציה!\n"
            "קדימה אלוף! 🏆"}
    ]
if "transferred" not in st.session_state:
    st.session_state.transferred = False

user_msgs = [m for m in st.session_state.messages if m["role"] == "user"]
if len(user_msgs) >= MAX_MESSAGES:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "🔄 התחלנו שיחה טרייה! קדימה, מה השאלה הבאה? 💪🔥"}
    ]

avatar = (
    f'<img src="data:image/jpeg;base64,{logo_b64}" '
    'style="width:44px;height:44px;border-radius:50%;object-fit:cover;border:2px solid #c0392b;">'
) if logo_b64 else "💪"

st.markdown(f"""
<div class="wa-header">
    {avatar}
    <div>
        <div class="wa-name">{GYM_NAME}</div>
        <div class="wa-status">⚡ מאמן {TRAINER_NAME} | מחובר</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    content = msg["content"] if isinstance(msg["content"], str) else "📸 תמונה"
    if msg["role"] == "user":
        st.markdown(
            f'<div class="msg-wrapper-user"><div class="msg-user">{content}'
            f'<div class="msg-time">✓✓</div></div></div>', unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="msg-wrapper-bot"><div class="msg-bot">{content}'
            f'<div class="msg-time">💪 {TRAINER_NAME} | {GYM_NAME}</div></div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.transferred:
    if st.button("📲 העבר אותי למאמן"):
        st.session_state.transferred = True
        wa_link = (
            f"https://wa.me/972{TRAINER_PHONE[1:]}"
            f"?text=היי+{TRAINER_NAME},+אני+מתאמן+ב{GYM_NAME}+וצריך+עזרה"
        )
        st.session_state.messages.append({
            "role": "assistant",
            "content": (
                f'בוודאי! 😊 לחץ כאן לשיחה ישירה עם {TRAINER_NAME}: '
                f'<a href="{wa_link}" target="_blank" style="color:#c0392b;font-weight:bold;">'
                f'💬 ווצאפ עם {TRAINER_NAME}</a>'
            )
        })
        st.rerun()

with st.expander("📸 שלח תמונה או וידאו (אוכל / תרגיל)"):
    uploaded = st.file_uploader(
        "בחר קובץ", type=["jpg", "jpeg", "png", "mp4", "mov"], label_visibility="collapsed"
    )
    if uploaded:
        if uploaded.type.startswith("image"):
            st.image(uploaded, width=220)
        else:
            st.video(uploaded)

        caption = st.text_input("הוסף הערה (לא חובה):", placeholder="למשל: מה הקלוריות כאן? / תבדוק לי את הטכניקה")

        if st.button("📤 שלח לבן"):
            text = caption if caption else "תנתח את זה מבחינת כושר/תזונה בקצרה"
            st.session_state.messages.append({"role": "user", "content": f"[מדיה] {text}"})

            with st.spinner("🔍 בן מנתח..."):
                if uploaded.type.startswith("image"):
                    img_b64 = base64.b64encode(uploaded.read()).decode()
                    mime = "image/jpeg" if uploaded.name.lower().endswith(("jpg", "jpeg")) else "image/png"
                    reply = analyze_image(img_b64, mime, text)
                else:
                    reply = call_api_smart(
                        st.session_state.messages + [{
                            "role": "user",
                            "content": f"קיבלתי קטע וידאו מהמתאמן. תיאורו: {text}. תן משוב כמאמן."
                        }]
                    )
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

if prompt := st.chat_input(f"שאל את {TRAINER_NAME}... 💪"):
    st.session_state.transferred = False
    st.session_state.messages.append({"role": "user", "content": prompt})

    thinking_placeholder = st.empty()
    thinking_placeholder.markdown(
        '<div class="msg-wrapper-bot"><div class="thinking-box">🔥 בן חושב...</div></div>',
        unsafe_allow_html=True
    )

    reply = call_api_smart(st.session_state.messages)

    thinking_placeholder.empty()
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

with st.sidebar:
    if logo_b64:
        st.image("logo.jpg", use_container_width=True)
    st.markdown(f"### {GYM_NAME}")
    st.markdown("💪 STRENGTH › FOCUS › RESULTS")
    st.markdown(f"📞 מאמן {TRAINER_NAME}: {TRAINER_PHONE}")
    st.divider()
    if st.button("🗑 שיחה חדשה"):
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "assistant", "content": f"היי! 👋 ברוך הבא ל-{GYM_NAME}! 🔥\nשאל אותי הכל! 💪"}
        ]
        st.session_state.transferred = False
        st.rerun()
