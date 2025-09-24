import streamlit as st
import cv2
from deepface import DeepFace
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="SoulSync",
    page_icon="🎵",
    layout="wide"
)

# --- Dummy Function ---
def get_dummy_recommendations(mood):
    dummy_data = {
        'happy': [
            {"artist": "Pharrell Williams", "name": "Happy", "url": "https://open.spotify.com/track/60nZcImufyM1siy4CVCDbM", "img": "https://i.scdn.co/image/ab67616d0000b273886369d835bd697205090146"},
            {"artist": "Katrina & The Waves", "name": "Walking on Sunshine", "url": "https://open.spotify.com/track/05wIrZSwuaVWhcv5F5e0lP", "img": "https://i.scdn.co/image/ab67616d0000b2730535b42d1754015205565573"},
            {"artist": "Queen", "name": "Don't Stop Me Now", "url": "https://open.spotify.com/track/5T8EDUDqKcs6OSOwEsfqG7", "img": "https://i.scdn.co/image/ab67616d0000b273e33b856e8285971167905188"}
        ],
        'sad': [
            {"artist": "Adele", "name": "Someone Like You", "url": "https://open.spotify.com/track/1zwMYTA5nlNjZxYrvBB2i7", "img": "https://i.scdn.co/image/ab67616d0000b2732118bf9b198b05a95dedf608"},
            {"artist": "Coldplay", "name": "Fix You", "url": "https://open.spotify.com/track/7LVHVU3tWfcxj5aiPFEW4Q", "img": "https://i.scdn.co/image/ab67616d0000b27351c02e90dec890335b8ea734"},
            {"artist": "Billie Eilish", "name": "when the party's over", "url": "https://open.spotify.com/track/43zdsphuZLzwA9k4DJhU0I", "img": "https://i.scdn.co/image/ab67616d0000b273ea32f195d31ea30504996414"}
        ],
        'neutral': [
            {"artist": "Bon Iver", "name": "Holocene", "url": "https://open.spotify.com/track/4fbvXwMTjqIIbvq7dJYleU", "img": "https://i.scdn.co/image/ab67616d0000b273a210a59a7b7a95577665242d"},
            {"artist": "The xx", "name": "Intro", "url": "https://open.spotify.com/track/2usrT8QIbIk9y0NEtQwS4j", "img": "https://i.scdn.co/image/ab67616d0000b273d2a7554304603625f32a7927"},
            {"artist": "Air", "name": "La Femme D'Argent", "url": "https://open.spotify.com/track/6tEaLp0eSjTfH7t4VQR54o", "img": "https://i.scdn.co/image/ab67616d0000b2733b1e85871e8f73167a5b3a4a"}
        ]
    }
    return dummy_data.get(mood.lower(), dummy_data['neutral'])

# --- App Title and Description ---
st.title("SoulSync: Your Emotion-Adaptive Music Player 🎵")
st.write("Let SoulSync analyze your mood and curate the perfect playlist for your moment.")

# --- Session State Initialization ---
if 'run' not in st.session_state:
    st.session_state.run = False
if 'current_mood' not in st.session_state:
    st.session_state.current_mood = "None"

def start_detection():
    st.session_state.run = True

def stop_detection():
    st.session_state.run = False

# --- UI Layout ---
left_col, right_col = st.columns([2, 3])

with left_col:
    st.header("Controls")
    st.button("Start Mood Detection", on_click=start_detection, type="primary", use_container_width=True)
    st.button("Stop", on_click=stop_detection, use_container_width=True)
    
    st.header(f"Detected Mood:")
    mood_placeholder = st.empty()
    mood_placeholder.subheader(st.session_state.current_mood)

with right_col:
    st.header("Live Feed & Recommendations")
    video_placeholder = st.empty()
    songs_placeholder = st.empty()
    
    # The button is now defined once, outside the loop.
    if st.session_state.run and st.session_state.current_mood not in ["No face detected", "None"]:
        if st.button("Create this playlist on Spotify", use_container_width=True, key="create_playlist"):
            st.success("Playlist created successfully! (Dummy feature)")
            st.balloons()

# --- Main Application Logic ---
if st.session_state.run:
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # --- THIS LINE IS NOW CORRECTED ---
    cap = cv2.VideoCapture(0)

    while cap.isOpened() and st.session_state.run:
        ret, frame = cap.read()
        if not ret:
            st.warning("Error: Could not read frame from webcam.")
            st.session_state.run = False # Stop the loop if camera fails
            break
        
        try:
            # We use a frame counter to analyze only every Nth frame to save resources
            frame_count = 0
            if frame_count % 5 == 0: # Analyze every 5th frame
                analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                dominant_emotion = analysis[0]['dominant_emotion'].capitalize()
                st.session_state.current_mood = dominant_emotion
            frame_count += 1
            
        except Exception as e:
            st.session_state.current_mood = "No face detected"
        
        # Update placeholders in every loop iteration
        mood_placeholder.subheader(st.session_state.current_mood)
        video_placeholder.image(frame, channels="BGR")
        
        if st.session_state.current_mood not in ["No face detected", "None"]:
            recommendations = get_dummy_recommendations(st.session_state.current_mood)
            with songs_placeholder.container():
                st.subheader("Here's a playlist for you:")
                for song in recommendations:
                    img_col, info_col = st.columns([1, 4])
                    with img_col:
                        st.image(song['img'], width=80)
                    with info_col:
                        st.write(f"**{song['name']}** by {song['artist']}")
                        st.markdown(f"[Listen on Spotify]({song['url']})", unsafe_allow_html=True)
        else:
            songs_placeholder.empty()

    cap.release()
    # Rerun to update button visibility after stopping
    st.rerun()

else:
    st.info("Click 'Start Mood Detection' to begin.")