import streamlit as st
import speech_recognition as sr
from PIL import Image

# Load and display the logo at the top of the app
logo = Image.open("image/Bayan_Interface_tp.png")  # Replace with the path to your logo file
st.image(logo, width=200)  # Adjust the width as needed

# Custom CSS for styling to match the Bayan PDF
st.markdown("""
    <style>
    body {
        background-color: #001f3f;
    }
    .css-18e3th9 {
        background-color: #001f3f;
    }
    .css-1d391kg p {
        color: #FFFFFF;
        font-size: 18px;
    }
    .css-10trblm {
        background-color: #FFFFFF;
    }
    h1 {
        color: #FF4136;
        font-size: 42px;
    }
    .stTextArea textarea {
        background-color: #F1F1F1;
        color: #111111;
    }
    .stSpinner {
        color: #FFDC00;
    }
    </style>
""", unsafe_allow_html=True)

# Title and introduction with colors matching Bayan theme
st.title("Bayan: Arabic Speech-to-Text")
st.write("**Welcome to Bayan**, a speech-to-text software designed for the Arabic language.")
st.write("Upload an audio file below to start.")

# Upload audio file
uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3"])

# Function to recognize speech from audio
def transcribe_audio(file):
    recognizer = sr.Recognizer()
    audio = sr.AudioFile(file)
    with audio as source:
        audio_data = recognizer.record(source)
        try:
            # Convert speech to text
            text = recognizer.recognize_google(audio_data, language="ar-SA")
            return text
        except sr.UnknownValueError:
            return "Sorry, speech could not be understood."
        except sr.RequestError as e:
            return f"API error: {e}"

# If the user uploads an audio file
if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")  # Handle different formats if necessary

    # Process the audio file
    with st.spinner("Transcribing..."):
        transcript = transcribe_audio(uploaded_file)
        st.write("Here is the transcribed text:")
        st.text_area("Transcript", transcript, height=250)

# Footer
st.write("Bayan: Bringing clarity to communication through Arabic Speech-to-Text.")
