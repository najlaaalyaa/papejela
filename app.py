import streamlit as st
import requests
import json
import base64
import random
import re
import os

# --- 1. SETUP PAGE ---
st.set_page_config(page_title="VibeChecker", page_icon="🎵", layout="wide")

# --- 2. IMAGE LOADER ---
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

# --- 3. CUSTOM CSS ---
img_base64 = get_base64_of_bin_file("background.jpeg")
if img_base64:
    background_style = f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)),
            url("data:image/jpeg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
    """
else:
    background_style = "<style>.stApp { background-color: #0E1117; }</style>"

st.markdown(background_style, unsafe_allow_html=True)

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.title-text {
    font-size: 70px; font-weight: 900; text-align: center;
    background: -webkit-linear-gradient(45deg, #00d2ff, #3a7bd5);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    padding-bottom: 20px;
}

.song-card {
    background-color: white; border-radius: 12px; padding: 15px;
    margin-bottom: 15px; display: flex; align-items: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}

.album-art {
    width: 60px; height: 60px; border-radius: 8px;
    margin-right: 15px; font-size: 30px;
    display: flex; align-items: center; justify-content: center;
}

.song-info { flex-grow: 1; color: #333; margin-right: 15px; }
.song-title { font-size: 18px; font-weight: 800; color: #000; }
.song-artist { font-size: 14px; font-weight: 600; color: #555; }

.listen-btn {
    background-color: white; color: #00d2ff;
    border: 2px solid #00d2ff; padding: 5px 15px;
    border-radius: 20px; font-weight: bold; font-size: 12px;
}
.listen-btn:hover { background-color: #00d2ff; color: white; }
</style>
""", unsafe_allow_html=True)

# --- 4. API SETUP ---
api_key = st.secrets.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠️ API Key missing!")
    st.stop()

# --- 5. STATE MANAGEMENT ---
if 'playlist' not in st.session_state: st.session_state.playlist = None
if 'error_debug' not in st.session_state: st.session_state.error_debug = None
if 'current_mood' not in st.session_state: st.session_state.current_mood = ""

# --- 6. THE BRAIN (MODIFIED ONLY LOGIC) ---
def get_vibe_check(mood):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}

    prompt = (
        f"User input: '{mood}'.\n\n"
        "Determine whether this input expresses a human mood or emotion.\n"
        "If YES, recommend 5 songs matching the vibe.\n"
        "If NO (random letters, numbers, symbols), return invalid.\n\n"
        "Return ONLY JSON.\n\n"
        "VALID FORMAT:\n"
        "[{\"title\":\"Song\",\"artist\":\"Artist\",\"link\":\"https://www.youtube.com/results?search_query=Song+Artist\"}]\n\n"
        "INVALID FORMAT:\n"
        "[{\"error\":\"invalid mood\"}]"
    )

    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        text = response.json()['candidates'][0]['content']['parts'][0]['text']

        match = re.search(r"\[.*\]", text, re.DOTALL)
        if not match:
            return "❌ Invalid AI response."

        parsed = json.loads(match.group(0))

        if isinstance(parsed, list) and "error" in parsed[0]:
            return "❌ Invalid mood. Please describe how you feel."

        return parsed

    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- 7. SIDEBAR ---
with st.sidebar:
    st.title("🎧 Control Panel")

    if st.button("🎲 Surprise Me"):
        vibe = random.choice(["Energetic", "Chill", "Melancholy", "Dreamy"])
        st.session_state.current_mood = vibe
        with st.spinner("Curating vibes..."):
            st.session_state.playlist = get_vibe_check(vibe)

    if st.button("🔄 Reset App"):
        st.session_state.playlist = None
        st.session_state.current_mood = ""
        st.session_state.error_debug = None
        st.rerun()

# --- 8. MAIN UI ---
st.markdown('<p class="title-text">🎵 VibeChecker</p>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
if c1.button("⚡ Energetic"): st.session_state.playlist = get_vibe_check("Energetic")
if c2.button("☂️ Melancholy"): st.session_state.playlist = get_vibe_check("Melancholy")
if c3.button("🧘 Chill"): st.session_state.playlist = get_vibe_check("Chill")
if c4.button("💔 Heartbroken"): st.session_state.playlist = get_vibe_check("Heartbroken")

# --- 9. USER INPUT (ENTER + SUBMIT FIXED, LAYOUT SAME) ---
with st.form("mood_form"):
    user_input = st.text_input("Or type your exact mood here...")
    submitted = st.form_submit_button("Submit")

if submitted and user_input.strip():
    st.session_state.current_mood = user_input
    with st.spinner(f"Analyzing mood: {user_input}..."):
        result = get_vibe_check(user_input)
        if isinstance(result, list):
            st.session_state.playlist = result
        else:
            st.session_state.error_debug = result

# --- 10. DISPLAY RESULTS ---
if st.session_state.error_debug:
    st.error(st.session_state.error_debug)

if st.session_state.playlist:
    st.write("---")
    st.markdown(f"### 🎶 Recommended for {st.session_state.current_mood}")

    emojis = ["🎵", "🎸", "🎹", "🎷", "🎧"]
    for song in st.session_state.playlist:
        st.markdown(f"""
        <div class="song-card">
            <div class="album-art">{random.choice(emojis)}</div>
            <div class="song-info">
                <div class="song-title">{song.get('title')}</div>
                <div class="song-artist">{song.get('artist')}</div>
            </div>
            <a href="{song.get('link')}" target="_blank" class="listen-btn">▶ Listen</a>
        </div>
        """, unsafe_allow_html=True)
