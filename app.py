import streamlit as st
import time
import os

# Try to import Gemini SDK with safe fallback
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ModuleNotFoundError:
    GEMINI_AVAILABLE = False

# ----------------------------
# Streamlit Page Config
# ----------------------------
st.set_page_config(
    page_title="VibeChecker",
    page_icon="🎵",
    layout="wide"
)

# Load CSS if exists
if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<h2>🎧 VibeChecker</h2>", unsafe_allow_html=True)
    st.markdown("Your elegant AI music curator.")

    st.write("### How to Use")
    st.write("Select a mood → AI generates playlist → Enjoy 🎶")

    st.write("---")
    st.write("### Surprise Me")
    st.button("🎲 Random Mood")

# ----------------------------
# Gemini Setup
# ----------------------------
if GEMINI_AVAILABLE:
    # Load key
    GEMINI_API_KEY = st.secrets.get("AIzaSyDWyAp3y6GsWfeQm3XSMit0UmRdQJAmJK0", None)

    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-pro")
    else:
        GEMINI_AVAILABLE = False
else:
    model = None

# ----------------------------
# AI Playlist Function
# ----------------------------
def generate_playlist(mood):
    if not GEMINI_AVAILABLE:
        return [
            ("AI Not Enabled", "Please install google-generativeai", "#"),
            ("Missing API Key", "Add GEMINI_API_KEY in Streamlit Secrets", "#")
        ]

    prompt = f"""
    Create a playlist of 6 songs based on mood: {mood}.
    Format each line as: Title - Artist.
    Do NOT add numbering.
    """
    
    response = model.generate_content(prompt)
    lines = response.text.strip().split("\n")

    playlist = []
    for line in lines:
        if "-" in line:
            title, artist = line.split("-", 1)
            playlist.append((title.strip(), artist.strip(), "#"))

    return playlist[:6]

# ----------------------------
# Show playlist cards
# ----------------------------
def display_playlist(mood):
    with st.spinner(f"Curating {mood} vibes… 🎶"):
        time.sleep(1.2)
        tracks = generate_playlist(mood)

    st.markdown(f"<h2>Recommended for {mood}</h2>", unsafe_allow_html=True)

    for title, artist, link in tracks:
        st.markdown(
            f"""
            <div class='card'>
                <div class='card-left'>
                    <div class='album-placeholder'></div>
                </div>
                <div class='card-right'>
                    <div class='song-title'>{title}</div>
                    <div class='song-artist'>{artist}</div>
                    <a href='{link}' target='_blank' class='listen-btn'>Listen</a>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ----------------------------
# UI Buttons
# ----------------------------
st.title("VibeChecker 🎵")
st.subheader("Your Mood-Based AI Music Curator")

col1, col2, col3, col4 = st.columns(4)
with col1:
    energetic = st.button("⚡ Energetic")
with col2:
    melancholy = st.button("🟣 Melancholy")
with col3:
    chill = st.button("🧘 Chill")
with col4:
    heartbroken = st.button("💔 Heartbroken")

user_mood = st.text_input("", placeholder="Type your mood…")

# Trigger
if energetic:
    display_playlist("Energetic")
elif melancholy:
    display_playlist("Melancholy")
elif chill:
    display_playlist("Chill")
elif heartbroken:
    display_playlist("Heartbroken")
elif user_mood:
    display_playlist(user_mood.title())
