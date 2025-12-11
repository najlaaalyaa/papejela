import streamlit as st
import time
import random
import google.generativeai as genai

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="VibeChecker",
    page_icon="🎵",
    layout="wide"
)

# =========================
# GEMINI CONFIG
# =========================
# Put your Gemini API key in .streamlit/secrets.toml as:
# GEMINI_API_KEY = "your_key_here"
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ GEMINI_API_KEY not found in Streamlit secrets. Please add it before running.")
else:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# =========================
# LOAD CUSTOM CSS
# =========================
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("⚠️ style.css not found. Create one in the same folder for full styling.")

# Floating icons
st.markdown("""
<div class="floating-icon">🎵</div>
<div class="floating-icon2">✨</div>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("<div class='sidebar-title'>🎧 VibeChecker</div>", unsafe_allow_html=True)
    st.markdown("<p class='sidebar-sub'>Your elegant AI music curator.</p>", unsafe_allow_html=True)

    st.markdown("### How to Use")
    st.markdown("""
    1. Tell me how you feel  
    2. I’ll understand your mood  
    3. I’ll curate songs for you 🎶  
    """)

    st.write("---")
    st.markdown("### Quick Moods")
    st.markdown("- Energetic\n- Chill\n- Melancholy\n- Heartbroken")

    st.write("---")
    surprise_me = st.button("🎲 Surprise Me")

# =========================
# MAIN TITLE
# =========================
st.markdown("<h1 class='title'>VibeChecker</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your AI Mood-Based Music Curator</p>", unsafe_allow_html=True)

st.write("")
st.write("")

# =========================
# MOOD BUTTONS
# =========================
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

# =========================
# USER MOOD INPUT
# =========================
user_mood = st.text_input(" ", placeholder="Tell me how you feel… (e.g. 'anxious but hopeful')")

# =========================
# GEMINI HELPERS
# =========================

def get_model():
    if "GEMINI_API_KEY" not in st.secrets:
        return None
    return genai.GenerativeModel("gemini-pro")

def validate_mood_input(user_text: str) -> bool:
    """
    Uses Gemini to check if the user is expressing an emotion or mood.
    Returns True if mood-related, False if off-topic.
    """
    model = get_model()
    if model is None:
        return False

    prompt = f"""
    The user said: "{user_text}"

    Your task:
    - Decide if this text is describing how the user feels (an emotion, mood, or state of mind).
    - Reply ONLY with "YES" if it is clearly a mood/feeling.
    - Reply ONLY with "NO" if it is a question, a request, random text, technical issue, or anything not describing their emotional state.

    Examples:
    - "i feel sad" → YES
    - "i'm bored" → YES
    - "i feel energetic today" → YES
    - "lonely but hopeful" → YES
    - "what is 5+5?" → NO
    - "how to cook rice?" → NO
    - "my streamlit app is broken" → NO
    - "open the door" → NO
    - "i like cats" → NO
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.strip().upper()
        return text.startswith("YES")
    except Exception as e:
        st.error(f"Validation error: {e}")
        return False

def get_ai_recommendations(mood_text: str):
    """
    Uses Gemini to generate a short playlist based on mood_text.
    Returns a list of (title, artist, link) tuples.
    """
    model = get_model()
    if model is None:
        return []

    prompt = f"""
    You are an AI music curator.

    User mood description:
    "{mood_text}"

    Recommend EXACTLY 5 songs that fit this mood.
    Use a mix of modern and classic tracks if suitable.

    Format each line EXACTLY like this (no bullet points, no numbering):
    Title - Artist - Suggested YouTube Link

    If you don't know the exact link, you can invent a plausible YouTube search URL like:
    https://www.youtube.com/results?search_query=Title+Artist

    Do NOT add any extra text, only 5 lines of recommendations.
    """

    try:
        response = model.generate_content(prompt)
        text = response.text

        lines = [line.strip() for line in text.split("\n") if "-" in line]
        songs = []

        for line in lines:
            parts = line.split(" - ")
            if len(parts) >= 2:
                title = parts[0].strip()
                artist = parts[1].strip()
                link = parts[2].strip() if len(parts) > 2 else ""
                songs.append((title, artist, link))

        return songs[:5]
    except Exception as e:
        st.error(f"Error getting recommendations: {e}")
        return []

def display_playlist(mood_text: str):
    """
    Shows cards with recommendations for the mood_text.
    """
    with st.spinner(f"Curating vibes for “{mood_text}” 🎶"):
        time.sleep(1)
        recs = get_ai_recommendations(mood_text)

    if not recs:
        st.error("I couldn't generate music recommendations right now. Try again or change your mood description.")
        return

    st.markdown(
        f"<h2 class='section-title'>Recommended for “{mood_text}”</h2>",
        unsafe_allow_html=True
    )

    for title, artist, link in recs:
        btn_html = f"<a href='{link}' target='_blank' class='listen-btn'>Listen</a>" if link else ""
        st.markdown(
            f"""
            <div class='card fade-in'>
                <div class='card-left'>
                    <div class='album-img-placeholder'>💿</div>
                </div>
                <div class='card-right'>
                    <div class='song-title'>{title}</div>
                    <div class='song-artist'>{artist}</div>
                    {btn_html}
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

# =========================
# EVENT HANDLING
# =========================

preset_moods = {
    "energetic": "high energy upbeat hype mood, feel like dancing or working out",
    "melancholy": "sad, reflective, slightly empty but calm",
    "chill": "relaxed, peaceful, want calm background vibes",
    "heartbroken": "broken heart, breakup pain, missing someone deeply"
}

# 1. Button moods (always valid)
if energetic:
    display_playlist(preset_moods["energetic"])
elif melancholy:
    display_playlist(preset_moods["melancholy"])
elif chill:
    display_playlist(preset_moods["chill"])
elif heartbroken:
    display_playlist(preset_moods["heartbroken"])
elif surprise_me:
    random_mood = random.choice(list(preset_moods.values()))
    display_playlist(random_mood)
# 2. Free text mood (must pass mood validation)
elif user_mood.strip():
    if validate_mood_input(user_mood.strip()):
        display_playlist(user_mood.strip())
    else:
        st.warning("✨ I can recommend music for you — but first tell me how you feel emotionally (e.g. 'sad but hopeful', 'stressed', 'super happy').")
