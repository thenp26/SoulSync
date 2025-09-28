# SoulSync 🎵

An AI-powered web application that detects your facial emotion in real-time and recommends a music playlist to match your mood.

Version 0.2 
updates : added a feature for detecting the dominant emotion from by capturing upto 20 emotion 

*(In one line: it's like having a DJ who is also your therapist... and also maybe your crush?)*



---

## ✨ Features

* **Real-Time Emotion Detection:** Uses your webcam to analyze your facial expression.
* **Dynamic UI:** A clean, two-column interface built with Streamlit.
* **Music Recommendations:** Displays a curated list of songs with album art and clickable Spotify links.

---

## 🛠️ Tech Stack

* **Python:** Core programming language.
* **Streamlit:** For the web application framework.
* **OpenCV:** For real-time video capture.
* **DeepFace:** For facial analysis and emotion recognition.
* **Spotipy:** (Optional, for real API integration) Client for the Spotify Web API.

---

## ⚙️ Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/thenp26/SoulSync.git](https://github.com/thnp26/SoulSync.git)
    cd SoulSync
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS / Linux
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

---
    
## 🔧 Configuration
    
*(Note: The current version uses dummy data. The steps below are for enabling the real Spotify API.)*
    
To use the Spotify API, you need to set up your credentials.
    
1.  Create an application on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2.  Create a `.env` file in the project's root directory.
3.  Add your credentials to the `.env` file:
    ```ini
    SPOTIPY_CLIENT_ID='Your_Client_ID'
    SPOTIPY_CLIENT_SECRET='Your_Client_Secret'
    SPOTIPY_REDIRECT_URI='[http://127.0.0.1:8080/callback](http://127.0.0.1:8080/callback)'
    ```

---

## ▶️ Usage

To run the application, execute the following command in your terminal:

```bash
streamlit run app.py

---
**🚀 Future Development
The next major update will connect the app directly to the Spotify API, allowing users to create playlists in their accounts. The final version of the project will be deployed and hosted on Streamlit Community Cloud for anyone to use!