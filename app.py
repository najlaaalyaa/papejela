import streamlit as st
import requests
import json
import base64
import random
import re
import os

# ---------------------------------------------------
# 1. PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="VibeChecker",
    page_icon="🎵",
    layout="wide"
)

# ---------------------------------------------------
# 2. BACKGROUND IMAGE LOADER
# ---------------------------------------------------
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

# ---------------------------------------------------
# 3. BACKGROUND + CSS
# ---------------------------------------------------
img_base64 = get_base64_of_bin_file("background.jpeg")

if img_base64:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
            linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)),
            url("data:image/jpeg;base64,{img_base64}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown("<style>.stApp { background-color: #0E1117; }</style>", unsafe_allow_html=True)

st.markdown("""
<style>
#MainMenu, footer {visibility: hidden;}

.title-text {
    font-size: 70px;
    font-weight: 900;
    text-align: center;
    background: -webkit-linear-gradient(45deg, #00d2ff, #3a7bd5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-bottom: 20px;
}

.song-card {
    background: white;
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}

.album-art {
    width: 60px;
    height: 60px;
    border-radius: 8px;
    margin-right: 15px;
    font-size: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.song-title {
    font-size: 18px;
    font-weight: 800;
    color: #000;
}

.song-artist {
    font-size: 14px;
    font-weight: 600;
    color: #555;
}

.listen-btn {
    background-color: white;
    color: #00d2ff;
    border: 2px solid #00d2ff;
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: bold;
    text-decoration: none;
}
.listen-btn:hover {
    background-color: #00d2ff;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# 4. API KEY
# ---------------------------------------------------
api_key = st.secrets.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ GOOGLE_API_KEY not found.")
    st.stop()

# ---------------------------------------------------
# 5. SESSION STATE
# ---------------------------------------------------
if "playlist" not in st.session_state:
    st.session_state.playlist = None
if "current_mood" not in st.session_state:
    st.session_state.current_mood = ""
if "error" not in st.session_state:
    st.session_state.error = None

# ---------------------------------------------------
# 6. AI BRAIN (VALIDATES MOOD)
# ---------------------------------------------------
def get_vibe_check(mood):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    prompt = f"""
You are an emotional-intent classifier and music recommender.

User input:
"{mood}"

STEP 1 — VALIDATION:
Determine whether the input expresses a human emotion, feeling, or mood.

VALID examples:
sad
tired but okay
overthinking at night
angry at myself
numb
idk how I feel

INVALID examples:
asdkj123
123456
$$$$
qwertyuiop
random unrelated words

STEP 2 — ACTION:
If VALID → recommend 5 songs that match the emotional vibe
If INVALID → return invalid response

OUTPUT RULES:
Return ONLY valid JSON
No explanation text

VALID FORMAT:
[
  {{
    "title": "Song Title",
    "artist": "Artist Name",
    "link": "https://www.youtube.com/results?search_query=Song+Artist"
  }}
]

INVALID FORMAT:
[
  {{
    "error": "invalid mood"
  }}
]
"""

    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        res = requests.post(url, json=data, timeout=20)
        text = res.json()["candidates"][0]["content"]["parts"][0]["text"]

        match = re.search(r"\[.*\]", text, re.DOTALL)
        if not match:
            return "❌ AI response error. Please try again."

        parsed = json.loads(match.group())

        if isinstance(parsed, list) and "error" in parsed[0]:
            return "❌ Invalid mood. Please describe how you feel."

        return parsed

    except Exception as e:
        return f"❌ Error: {e}"

# ---------------------------------------------------
# 7. SIDEBAR
# ---------------------------------------------------
with st.sidebar:
    st.title("🎧 Control Panel")

    if st.button("🎲 Surprise Me"):
        mood = random.choice(["Energetic", "Chill", "Melancholy", "Dreamy"])
        st.session_state.current_mood = mood
        with st.spinner("Curating vibes..."):
            st.session_state.playlist = get_vibe_check(mood)

    if st.button("🔄 Reset"):
        st.session_state.playlist = None
        st.session_state.current_mood = ""
        st.session_state.error = None
        st.rerun()

# ---------------------------------------------------
# 8. MAIN UI
# ---------------------------------------------------
st.markdown('<p class="title-text">🎵 VibeChecker</p>', unsafe_allow_html=True)

# ---------------------------------------------------
# 9. ENTER-KEY MOOD INPUT
# ---------------------------------------------------
st.write("### 🧠 Describe your mood")

with st.form("mood_form"):
    user_input = st.text_input(
        "Type how you feel and press Enter",
        placeholder="sad, tired but okay, numb, overthinking"
    )
    submitted = st.form_submit_button("Submit")

if submitted and user_input.strip():
    st.session_state.current_mood = user_input
    st.session_state.playlist = None
    st.session_state.error = None

    with st.spinner("Understanding your vibe..."):
        result = get_vibe_check(user_input)

        if isinstance(result, list):
            st.session_state.playlist = result
        else:
            st.session_state.error = result

# ---------------------------------------------------
# 10. DISPLAY RESULTS
# ---------------------------------------------------
if st.session_state.error:
    st.error(st.session_state.error)

if isinstance(st.session_state.playlist, list):
    st.markdown(f"### 🎶 Recommended for *{st.session_state.current_mood}*")

    emojis = ["🎵", "🎸", "🎹", "🎷", "🎧"]
    for song in st.session_state.playlist:
        st.markdown(f"""
        <div class="song-card">
            <div class="album-art">{random.choice(emojis)}</div>
            <div style="flex-grow:1">
                <div class="song-title">{song['title']}</div>
                <div class="song-artist">{song['artist']}</div>
            </div>
            <a class="listen-btn" href="{song['link']}" target="_blank">▶ Listen</a>
        </div>
        """, unsafe_allow_html=True)
