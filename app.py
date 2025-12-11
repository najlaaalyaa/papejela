import streamlit as st
import time
import random

# Page config
st.set_page_config(
    page_title="VibeChecker",
    page_icon="🎵",
    layout="wide"
)

# Load custom CSS
# Ensure you have a style.css file in the same directory
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
    surprise_me = st.button("🎲 Surprise Me")

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

# ---- Recommendation Data (Real Songs) ----
# Format: (Title, Artist/Channel, YouTube URL)
mood_data = {
    "Energetic": [
        ("Houdini", "Dua Lipa", "https://www.youtube.com/watch?v=suAR1PYFNYA"),
        ("Espresso", "Sabrina Carpenter", "https://www.youtube.com/watch?v=51zjlMhdSTE"),
        ("2024 Hits Mashup", "Logan Alexandra", "https://www.youtube.com/watch?v=29zyVX_iyHc")
    ],
    "Melancholy": [
        ("What Was I Made For?", "Billie Eilish", "https://www.youtube.com/watch?v=cW8VLC9nnTo"),
        ("Sad Songs Playlist", "Love Letter", "https://www.youtube.com/watch?v=mh2265QqV-Y"),
        ("Vampire (Official)", "Olivia Rodrigo", "https://www.youtube.com/watch?v=RlPNh_9IK0M")
    ],
    "Chill": [
        ("Good Days", "SZA", "https://www.youtube.com/watch?v=2p3zZoraK9g"),
        ("Tadow", "Masego & FKJ", "https://www.youtube.com/watch?v=hC8CH0Z3L54"),
        ("Lofi Pop 2024", "Hi-lofi", "https://www.youtube.com/watch?v=_sT0akYdxDQ")
    ],
    "Heartbroken": [
        ("you broke me first", "Tate McRae", "https://www.youtube.com/watch?v=QXzC2eiHBG8"),
        ("Residuals", "Chris Brown", "https://www.youtube.com/watch?v=46p-IxAVJ74"),
        ("Someone You Loved", "Lewis Capaldi", "https://www.youtube.com/watch?v=bCuhuePlP8o")
    ]
}

# ---- Recommendation Logic ----
def show_recs(mood):
    # Normalize mood string for dictionary lookup
    mood_key = mood.title() if mood.title() in mood_data else "Chill"  # Default to Chill if unknown
    
    # Specific override for user text input if it matches our keys
    if mood.title() in mood_data:
        recs = mood_data[mood.title()]
    else:
        # Fallback/Generic for custom text inputs
        recs = mood_data["Chill"] 

    # Loading animation
    with st.spinner(f"Curating {mood} vibes… 🎶"):
        time.sleep(1.0) # Slightly faster

    st.markdown(f"<h2 class='section-title'>Recommended for {mood}</h2>", unsafe_allow_html=True)

    # Display recommendation cards
    for title, artist, link in recs:
        st.markdown(
            f"""
            <div class='card fade-in'>
                <div class='card-left'>
                    <div class='album-placeholder'>💿</div>
                </div>
                <div class='card-right'>
                    <div class='song-title'>{title}</div>
                    <div class='song-artist'>{artist}</div>
                    <a href='{link}' target='_blank' class='listen-btn'>Listen on YouTube</a>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Now playing bar (Shows the first song in the list)
    st.markdown(
        f"""
        <div class='now-playing'>
            <span class='np-label'>Now Playing:</span> {recs[0][0]} — {recs[0][1]}
        </div>
        """,
        unsafe_allow_html=True
    )

# ---- Event Handling ----

if energetic:
    show_recs("Energetic")
elif melancholy:
    show_recs("Melancholy")
elif chill:
    show_recs("Chill")
elif heartbroken:
    show_recs("Heartbroken")
elif surprise_me:
    # Pick a random mood from the keys
    random_mood = random.choice(list(mood_data.keys()))
    show_recs(random_mood)
elif user_mood:
    # If the user types a mood we know, show it. Otherwise defaults to Chill logic above.
    # You could expand this with an API call in a real app!
    show_recs(user_mood)


