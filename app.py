import streamlit as st
import requests
import json
import base64
import random
import re
import os

# ---------------------------------------------------
# 1. PAGE SETUP
# ---------------------------------------------------
st.set_page_config(
    page_title="VibeChecker",
    page_icon="🎵",
    layout="wide"
)

# ---------------------------------------------------
# 2. IMAGE LOADER
# ---------------------------------------------------
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

# ---------------------------------------------------
# 3. BACKGROUND & CSS
# ---------------------------------------------------
img_base64 = get_base64_of_bin_file("background.jpeg")

if img_base64:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)),
            url("data:image/jpeg;base64,{img_base64}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<style>.stApp { background-color: #0E1117; }</style>",
        unsafe_allow_html=True
    )

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
    background-color: white;
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
# 6. AI BRAIN (FIXED)
# ---------------------------------------------------
def get_vibe_check(mood):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    prompt = f"""
You are a music recommendation AI.

User mood:
"{mood}"

Understand the emotional meaning (even if poetic or casual).
Recommend 5 songs that match the vibe.

RULES:
- Return ONLY valid JSON
- No explanations
- Format exactly like this:

[
  {{
    "title": "Song Name",
    "artist": "Artist",
    "link": "https://www.youtube.com/results?search_query=Song+Artist"
  }}
]

If mood is random or meaningless, return:
[{{"error":"invalid"}}]
"""

    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        res = requests.post(url, json=data, timeout=20)
        text = res.json()["candidates"][0]["content"]["parts"][0]["text"]

        match = re.search(r"\[.*\]", text, re.DOTALL)
        if not match:
            return "❌ Invalid AI response."

        parsed = json.loads(match.group())

        if "error" in parsed[0]:
            return "❌ Please describe your mood more clearly."

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

c1, c2, c3, c4 = st.columns(4)

if c1.button("⚡ Energetic"):
    st.session_state.current_mood = "Energetic"
    st.session_state.playlist = get_vibe_check("Energetic")

if c2.button("☂️ Melancholy"):
    st.session_state.current_mood = "Melancholy"
    st.session_state.playlist = get_vibe_check("Melancholy")

if c3.button("🧘 Chill"):
    st.session_state.current_mood = "Chill"
    st.session_state.playlist = get_vibe_check("Chill")

if c4.button("💔 Heartbroken"):
    st.session_state.current_mood = "Heartbroken"
    st.session_state.playlist = get_vibe_check("Heartbroken")

# ---------------------------------------------------
# 9. FREE TEXT MOOD INPUT (FIXED)
# ---------------------------------------------------
st.write("### 🧠 Describe your mood")
user_input = st.text_input(
    "Example: lonely but peaceful, late night overthinking, angry but motivated"
)

if st.button("🎯 Get Recommendations") and user_input.strip():
    st.session_state.current_mood = user_input
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
    st.markdown(f"### 🎶 Recommended for: *{st.session_state.current_mood}*")

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
