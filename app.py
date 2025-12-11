import streamlit as st
import time
import random

try:
    import google.generativeai as genai
except ImportError:
    st.error("Missing required package: google-generativeai. Please install it via pip.")
    st.stop()

# ---------------------------------------------------------
# Page Config
# ---------------------------------------------------------
st.set_page_config(
    page_title="VibeChecker",
    page_icon="🎵",
    layout="wide"
)

# Load CSS
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("⚠ style.css not found. Styling disabled.")

# Decorative Icons
st.markdown("""
<div class="floating-icon">🎵</div>
<div class="floating-icon2">✨</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("<div class='sidebar-title'>🎧 VibeChecker</div>", unsafe_allow_html=True)
    st.markdown("<p class='sidebar-sub'>Your elegant AI music curator.</p>", unsafe_allow_html=True)

    st.markdown("### How to Use")
    st.markdown("""
    1. Select a mood  
    2. AI curates songs  
    3. Enjoy the playlist 🎶  
    """)

    st.write("---")
    st.markdown("### Past Moods")
    st.markdown("- Melancholy\n- Chill\n- Energetic")

    st.write("---")
    surprise_me = st.button("🎲 Surprise Me")

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.markdown("<h1 class='title'>VibeChecker</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your Personal Mood-Based Music Curator</p>", unsafe_allow_html=True)

st.write("")
st.write("")

# ---------------------------------------------------------
# Mood Buttons
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    energetic = st.button("⚡ Energetic", use_container_width=True)
with col2:
    melancholy = st.button("🟣 Melancholy", use_container_width=True)
with col3:
    chill = st.button("🧘 Chill", use_container_width=True)
with col4:
    heartbroken = st.button("💔 Heartbroken", use_container_width=True)

st.write("")
user_mood = st.text_input(" ", placeholder="Type your mood here…")

# ---------------------------------------------------------
# Gemini Song Recommendation Logic
# ---------------------------------------------------------
def get_recommendations(mood):
    genai.configure(api_key=st.secrets["api_key"])
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    You are a highly specialized music curator. Suggest exactly 5 REAL and POPULAR songs that perfectly match the mood: "{mood}".

    Requirements:
    - Songs must strongly fit the emotional tone
    - No repeated artists
    - Must be recognizably accurate for the mood
    - Format EXACTLY like this:
      1. "Song Title" by Artist Name
    """

    try:
        response = model.generate_content(prompt)
        lines = response.text.strip().split("\n")

        recs = []
        for line in lines:
            if '"' in line and " by " in line:
                try:
                    title = line.split('"')[1].strip()
                    artist = line.split(" by ")[1].strip()
                except:
                    continue

                query = f"{title} {artist}".replace(" ", "+")
                yt_link = f"https://www.youtube.com/results?search_query={query}"

                recs.append((title, artist, yt_link))

        return recs[:5]

    except Exception as e:
        st.error("❌ Could not get song recommendations — check API key or internet.")
        st.stop()

# ---------------------------------------------------------
# Display Recommendations
# ---------------------------------------------------------
def show_recs(mood):
    recs = get_recommendations(mood)

    with st.spinner(f"Curating {mood} vibes… 🎶"):
        time.sleep(1)

    st.markdown(f"<h2 class='section-title'>Recommended for {mood}</h2>", unsafe_allow_html=True)

    for title, artist, link in recs:
        st.markdown(
            f"""
            <div class='card fade-in'>
                <div class='card-left'>
                    <div class='album-img-placeholder'>💿</div>
                </div>
                <div class='card-right'>
                    <div class='song-title'>{title}</div>
                    <div class='song-artist'>{artist}</div>
                    <a href='{link}' target='_blank' class='listen-btn'>Search on YouTube</a>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class='now-playing'>
            <span class='np-label'>Now Playing:</span> {recs[0][0]} — {recs[0][1]}
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------------
# Event System
# ---------------------------------------------------------
if energetic:
    show_recs("Energetic")
elif melancholy:
    show_recs("Melancholy")
elif chill:
    show_recs("Chill")
elif heartbroken:
    show_recs("Heartbroken")
elif surprise_me:
    mood = random.choice(["Energetic", "Melancholy", "Chill", "Heartbroken", "Happy", "Sad", "Romantic"])
    show_recs(mood)
elif user_mood:
    show_recs(user_mood)
