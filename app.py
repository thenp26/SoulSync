import streamlit as st
import cv2
from deepface import DeepFace
import pandas as pd
from collections import Counter

# --- Page Configuration ---
st.set_page_config(
    page_title="SoulSync v0.2",
    page_icon="🎶",
    layout="wide"
)


# --- Dummy Function (from v0.1) ---
def get_dummy_recommendations(mood):
    dummy_data = {
        'happy': [{"artist": "Pharrell Williams", "name": "Happy"}, {"artist": "Queen", "name": "Don't Stop Me Now"}],
        'sad': [{"artist": "Adele", "name": "Someone Like You"}, {"artist": "Coldplay", "name": "Fix You"}],
        'neutral': [{"artist": "Bon Iver", "name": "Holocene"}, {"artist": "The xx", "name": "Intro"}],
        'angry': [{"artist": "System Of A Down", "name": "B.Y.O.B."},
                  {"artist": "Rage Against The Machine", "name": "Killing In The Name"}],
        'surprise': [{"artist": "MGMT", "name": "Electric Feel"}, {"artist": "Daft Punk", "name": "One More Time"}]
    }
    return dummy_data.get(mood.lower(), dummy_data['neutral'])


# --- App Title and Description ---
st.title("SoulSync v0.2: Mood Aggregation 🎶")
st.write("SoulSync will now capture your mood over a short period to find the perfect playlist for you.")

# --- NEW: Expanded Session State Initialization ---
if 'run' not in st.session_state:
    st.session_state.run = False
if 'emotions_list' not in st.session_state:
    st.session_state.emotions_list = []
if 'capture_complete' not in st.session_state:
    st.session_state.capture_complete = False
if 'final_mood' not in st.session_state:
    st.session_state.final_mood = None


# --- NEW: Callback functions for buttons ---
def start_detection():
    # Reset all states for a fresh run
    st.session_state.run = True
    st.session_state.emotions_list = []
    st.session_state.capture_complete = False
    st.session_state.final_mood = None


def stop_detection():
    st.session_state.run = False


# --- UI Layout ---
left_col, right_col = st.columns([2, 3])

with left_col:
    st.header("Controls")
    # Use the 'disabled' parameter to control button availability
    st.button("Start Mood Scan", on_click=start_detection, type="primary", use_container_width=True,
              disabled=st.session_state.run)
    st.button("Stop Scan", on_click=stop_detection, use_container_width=True, disabled=not st.session_state.run)

    # NEW: Display final mood or progress
    if st.session_state.capture_complete:
        st.header("Dominant Mood:")
        st.subheader(f"✨ {st.session_state.final_mood} ✨")
        # The new "Reset" button is the same as the "Start" button
        st.button("Start New Scan", on_click=start_detection, use_container_width=True)
    elif st.session_state.run:
        st.header("Scan Progress:")
        progress_text = f"Capturing emotion {len(st.session_state.emotions_list)} of 20..."
        st.write(progress_text)
        st.progress(len(st.session_state.emotions_list) / 20)

with right_col:
    st.header("Live Feed & Recommendations")
    video_placeholder = st.empty()
    songs_placeholder = st.empty()

# --- Main Application Logic ---
if st.session_state.run:
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    while cap.isOpened() and st.session_state.run:
        ret, frame = cap.read()
        if not ret:
            st.warning("Error: Could not read frame from webcam.")
            break

        # Analyze emotion
        try:
            analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            dominant_emotion = analysis[0]['dominant_emotion'].capitalize()
            st.session_state.emotions_list.append(dominant_emotion)

            # --- NEW: Check if we have collected 20 emotions ---
            if len(st.session_state.emotions_list) >= 20:
                # Calculate the most common emotion
                mood_counts = Counter(st.session_state.emotions_list)
                st.session_state.final_mood = mood_counts.most_common(1)[0][0]

                # Set flags to stop the capture
                st.session_state.capture_complete = True
                st.session_state.run = False
                break  # Exit the while loop

        except Exception as e:
            # Briefly show "no face" but don't add it to the list
            pass

        video_placeholder.image(frame, channels="BGR")

    cap.release()
    st.rerun()  # Rerun the script to update the UI state after the loop stops

# Display final recommendations if capture is complete
if st.session_state.capture_complete:
    video_placeholder.info("Scan complete! Here are your recommendations.")
    with songs_placeholder.container():
        st.subheader(f"Playlist for a '{st.session_state.final_mood}' mood:")
        recommendations = get_dummy_recommendations(st.session_state.final_mood)
        df = pd.DataFrame(recommendations)
        st.dataframe(df, use_container_width=True)
else:
    if not st.session_state.run:
        video_placeholder.info("Click 'Start Mood Scan' to begin.")