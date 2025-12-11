import streamlit as st
import time

# Page config
st.set_page_config(
    page_title="VibeChecker",
    page_icon="🎵",
    layout="wide"
)

# Load custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Floating icons
st.markdown("""
<div class="floating-icon">🎵</div>
<div class="floating-icon2">✨</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("<div class='sidebar-title'>🎧 VibeChecker</div>", unsafe_allow_html=True)
    st.markdown("<p class='sidebar-sub'>Your elegant AI music curator.</p>", unsafe_allow_html=True)

    st.markdown("### How to Use")
    st.markdown("""
    1. Select a mood  
    2. Let me curate  
    3. Enjoy the playlist  
    """)

    st.write("---")
    st.markdown("### Past Moods")
    st.markdown("- Melancholy\n- Chill\n- Energetic")

    st.write("---")
    st.button("🎲 Surprise Me")

# --- Main Layout ---
st.markdown("<h1 class='title'>VibeChecker</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your Personal Mood-Based Music Curator</p>", unsafe_allow_html=True)

st.write("")
st.write("")

# Mood Buttons Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    energetic = st.button("⚡ Energetic", key="energetic", use_container_width=True)
with col2:
    melancholy = st.button("🟣 Melancholy", key="melancholy", use_container_width=True)
with col3:
    chill = st.button("🧘 Chill", key="chill", use_container_width=True)
with col4:
    heartbroken = st.button("💔 Heartbroken", key="heartbroken", use_container_width=True)

st.write("")
st.write("")

# Text Input Mood
user_mood = st.text_input(" ", placeholder="Type your mood here…")

# ---- Recommendation Logic ----
def show_recs(mood):
    # Loading animation
    with st.spinner(f"Curating {mood} vibes… 🎶"):
        time.sleep(1.5)

    st.markdown(f"<h2 class='section-title'>Recommended for {mood}</h2>", unsafe_allow_html=True)

    recs = [
        ("Soft Skies", "Eden Waves", "https://youtu.be/xxxx"),
        ("Golden Hour", "JVKE", "https://youtu.be/yxW5yuzVi8w"),
        ("Peaceful Mind", "Calm Collective", "https://youtu.be/xxxx")
    ]

    # Display recommendation cards
    for title, artist, link in recs:
        st.markdown(
            f"""
            <div class='card fade-in'>
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

    # Now playing bar
    st.markdown(
        f"""
        <div class='now-playing'>
            <span class='np-label'>Now Playing:</span> {recs[0][0]} — {recs[0][1]}
        </div>
        """,
        unsafe_allow_html=True
    )


# Trigger events
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
