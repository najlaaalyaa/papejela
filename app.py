import streamlit as st
import requests
import json
import base64
import random
import re
import os

# ======================================================
# 1. PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="VibeChecker",
    page_icon="🎵",
    layout="wide"
)

# ======================================================
# 2. BACKGROUND IMAGE LOADER
# ======================================================
def get_base64_of_bin_file(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

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
            background-position: center;
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

# ======================================================
# 3. CUSTOM CSS
# ======================================================
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

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
    background-color: #f0f2f6;
    border-radius: 8px;
    margin-right: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
}

.song-info {
    flex-grow: 1;
    color: #333;
}

.song-title {
    font-size: 18px;
    font-weight: 800;
    margin: 0;
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
    text-decoration: none;
    font-weight: bold;
    font-size: 12px;
}

.listen-btn:hover {
    background-color: #00d2ff;
    color: white;
}

.stButton button {
    width: 100%;
    height: 50px;
    border-radius: 10px;
    font-weight: 600;
    background-color: rgba(20,20,20,0.8);
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# 4. API KEY
# ======================================================
api_key = st.secrets.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ GOOGLE_API_KEY is missing.")
    st.stop()

# ======================================================
# 5. SESSION STATE
# ======================================================
if "playlist" not in st.session_state:
    st.session_state.playlist = None

if "error" not in st.session_state:
    st.session_state.error = None

if "current_mood" not in st.session_state:
    st.session_state.current_mood = ""

# ======================================================
# 6. AI FUNCTION
# ======================================================
def get_vibe_check(user_text):
    user_text = user_text.strip()[:120]

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/gemini-flash-latest:generateContent?key={api_key}"
    )

    prompt = (
        f"Analyze the emotional vibe from this user text:\n"
        f"'{user_text}'\n\n"
        "RULES:\n"
        "1. Return ONLY valid JSON.\n"
        "2. Output a JSON array of EXACTLY 5 songs.\n"
        "3. Each item must include: title, artist, link.\n"
        "4. No markdown, no explanations, no extra text."
    )

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            return f"API Error {response.status_code}"

        text = response.json()["candidates"][0]["content"]["parts"][0]["text"]

        # Try direct JSON
        try:
            return json.loads(text)
        except:
            pass

        # Fallback: extract JSON array
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))

        return "Invalid AI response"

    except Exception as e:
        return str(e)

# ======================================================
# 7. SIDEBAR
# ======================================================
with st.sidebar:
    st.title("🎧 VibeChecker")
    st.info("AI-powered mood-based music")

    if st.button("🔄 Reset"):
        st.session_state.playlist = None
        st.session_state.error = None
        st.session_state.current_mood = ""

# ======================================================
# 8. MAIN UI
# ======================================================
st.markdown('<p class="title-text">🎵 VibeChecker</p>', unsafe_allow_html=True)

st.write("### 🎧 Describe your mood")
user_input = st.text_input(
    "Type how you feel (e.g. calm night vibes, stressed but hopeful, heartbroken...)"
)

if st.button("Analyze My Mood 🎶") and user_input.strip():
    st.session_state.current_mood = user_input.strip()
    st.session_state.playlist = None
    st.session_state.error = None

    with st.spinner("Curating your vibe..."):
        result = get_vibe_check(user_input)

        if isinstance(result, list):
            st.session_state.playlist = result
        else:
            st.session_state.error = result

# ======================================================
# 9. OUTPUT
# ======================================================
if st.session_state.error:
    st.error(st.session_state.error)

if st.session_state.playlist:
    st.write("---")
    st.markdown(f"### 🎶 Recommended for: *{st.session_state.current_mood}*")

    emojis = ["🎵", "🎸", "🎹", "🎧", "🎷"]

    for song in st.session_state.playlist:
        st.markdown(
            f"""
            <div class="song-card">
                <div class="album-art">{random.choice(emojis)}</div>
                <div class="song-info">
                    <div class="song-title">{song.get("title","Track")}</div>
                    <div class="song-artist">{song.get("artist","Artist")}</div>
                </div>
                <a class="listen-btn" href="{song.get("link","#")}" target="_blank">
                    ▶ Listen
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
