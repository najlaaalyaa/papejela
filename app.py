import streamlit as st
import time
import random

try:
    import google.generativeai as genai
except ImportError:
    st.error("Missing required package: google-generativeai. Please install it via pip or add to requirements.txt.")
    st.stop()

# Page config
st.set_page_config(
    page_title="VibeChecker",
    page_icon="🎵",
    layout="wide"
)

# Load custom CSS
# Ensure you have a style.css file in the same directory
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("style.css not found. Skipping custom styles.")

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

# ---- Recommendation Logic ----
def get_recommendations(mood):
    # Configure Gemini API
    genai.configure(api_key=st.secrets["AIzaSyDWyAp3y6GsWfeQm3XSMit0UmRdQJAmJK0"])
    model = genai.GenerativeModel('gemini-1.5-flash')  # Use the appropriate model
    
    # Prompt to generate song recommendations
    prompt = f"""
    Suggest 5 popular songs that match the mood '{mood}'. For each song, provide the title and artist in the format:
    1. "Song Title" by Artist Name
    2. "Song Title" by Artist Name
    etc.
    Make sure the suggestions are real songs and relevant to the mood.
    """
    
    try:
        response = model.generate_content(prompt)
        suggestions = response.text.strip().split('\n')
        
        recs = []
        for suggestion in suggestions:
            if suggestion.strip():
                # Parse the suggestion (e.g., "1. "Song Title" by Artist Name")
                parts = suggestion.split(' by ', 1)
                if len(parts) == 2:
                    title = parts[0].strip().lstrip('0123456789. ').strip('"')
                    artist = parts[1].strip()
                    # Create a YouTube search link
                    search_query = f"{title} {artist}".replace(' ', '+')
                    link = f"https://www.youtube.com/results?search_query={search_query}"
                    recs.append((title, artist, link))
        return recs[:5]  # Limit to 5
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        # Fallback to a default set
        return [
            ("Default Song 1", "Default Artist", "https://www.youtube.com/results?search_query=Default+Song+1+Default+Artist"),
            ("Default Song 2", "Default Artist", "https://www.youtube.com/results?search_query=Default+Song+2+Default+Artist"),
            ("Default Song 3", "Default Artist", "https://www.youtube.com/results?search_query=Default+Song+3+Default+Artist")
        ]

def show_recs(mood):
    recs = get_recommendations(mood)
    
    # Loading animation
    with st.spinner(f"Curating {mood} vibes… 🎶"):
        time.sleep(1.0)  # Slightly faster

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
                    <a href='{link}' target='_blank' class='listen-btn'>Search on YouTube</a>
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
    # Pick a random mood from a list
    random_mood = random.choice(["Energetic", "Melancholy", "Chill", "Heartbroken", "Happy", "Sad"])
    show_recs(random_mood)
elif user_mood:
    # For custom moods, generate recommendations
    show_recs(user_mood)
