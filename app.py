import streamlit as st
import time
import google.generativeai as genai
import base64
from io import BytesIO
import random

# ------------------------------
# GEMINI SETUP
# ------------------------------
genai.configure(api_key="AIzaSyDWyAp3y6GsWfeQm3XSMit0UmRdQJAmJK0")

text_model = genai.GenerativeModel("gemini-1.5-flash")
vision_model = genai.GenerativeModel("gemini-1.5-pro")


# ------------------------------
# GENERATE PLAYLIST (TEXT)
# ------------------------------
def get_ai_playlist(mood):
    prompt = f"""
    Generate 5 song recommendations based on this mood: {mood}.
    Strict format only:

    Title | Artist | YouTube Link
    """

    response = text_model.generate_content(prompt)
    lines = response.text.split("\n")

    playlist = []
    for line in lines:
        if "|" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 3:
                playlist.append((parts[0], parts[1], parts[2]))

    return playlist


# ------------------------------
# GENERATE ALBUM ART (AI IMAGE)
# ------------------------------
def generate_album_art(title, artist, mood):
    prompt = f"""
    Generate an aesthetic square album cover in high quality based on this song:

    Title: {title}
    Artist: {artist}
    Mood theme: {mood}

    Style: cinematic, soft lighting, gradient glow, clean minimalistic aesthetic.
    No text on the image.
    """

    img = vision_model.generate_content(prompt, stream=False)
    image_bytes = img._result.candidates[0].content.parts[0].inline_data.data
    return image_bytes


def image_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")


# ------------------------------
# STREAMLIT PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="VibeChecker", page_icon="🎵", layout="wide")

# Load CSS
with open("style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ------------------------------
# SIDEBAR
# ------------------------------
with st.sidebar:
    st.markdown("<div class='sidebar-title'>🎧 VibeChecker</div>", unsafe_allow_html=True)
    st.markdown("<p class='sidebar-sub'>Your elegant AI music curator.</p>", unsafe_allow_html=True)

    st.markdown("### How to Use")
    st.markdown("""
    1. Select a mood  
    2. AI generates playlist  
    3. Enjoy the music  
    """)

    st.write("---")
    st.markdown("### Past Moods")
    st.markdown("- Melancholy\n- Chill\n- Energetic")

    st.write("---")

    # Surprise Me
    surprise = st.button("🎲 Surprise Me")
    if surprise:
        mood = random.choice(["Energetic", "Melancholy", "Chill", "Heartbroken", "Romantic", "Nostalgic", "Soft", "Dark"])
        st.session_state["surprise_mood"] = mood
    else:
        st.session_state["surprise_mood"] = None


# ------------------------------
# TITLE
# ------------------------------
st.markdown("<h1 class='title'>VibeChecker</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your Personal Mood-Based Music Curator</p>", unsafe_allow_html=True)

st.write("")
st.write("")


# ------------------------------
# MOOD BUTTONS
# ------------------------------
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
st.write("")

# Mood input
user_mood = st.text_input(" ", placeholder="Type your mood here…")


# ------------------------------
# SHOW RECOMMENDATIONS
# ------------------------------
def show_recs(mood):
    with st.spinner(f"Curating {mood} vibes… 🎶"):
        time.sleep(1.2)
        playlist = get_ai_playlist(mood)

    st.markdown(f"<h2 class='section-title'>Recommended for {mood}</h2>", unsafe_allow_html=True)

    for title, artist, link in playlist:

        # Generate AI album art
        img_bytes = generate_album_art(title, artist, mood)
        b64_img = image_to_base64(img_bytes)

        st.markdown(
            f"""
            <div class='card fade-in'>
                <div class='card-left'>
                    <img src="data:image/png;base64,{b64_img}" class="album-img"/>
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

    # Now Playing bar
    if playlist:
        st.markdown(
            f"""
            <div class='now-playing'>
                <span class='np-label'>Now Playing:</span> {playlist[0][0]} — {playlist[0][1]}
            </div>
            """,
            unsafe_allow_html=True
        )


# ------------------------------
# TRIGGERS
# ------------------------------
if energetic:
    show_recs("Energetic")
elif melancholy:
    show_recs("Melancholy")
elif chill:
    show_recs("Chill")
elif heartbroken:
    show_recs("Heartbroken")
elif user_mood:
    show_recs(user_mood.title())
elif st.session_state.get("surprise_mood"):
    show_recs(st.session_state["surprise_mood"])
