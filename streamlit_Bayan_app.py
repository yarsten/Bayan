import os
import streamlit as st
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from io import BytesIO
from PIL import Image
import openai
from st_audiorec import st_audiorec

# Load and display the logo at the top of the app
logo = Image.open("/home/yara/code/yarsten/Bayan/bayan/interface/image/Bayan_Interface_tp.png")
st.image(logo, width=400)

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #001f3f;
    }
    h1 {
        color: #68bdb2;
        font-size:55px;
    }
    .stTextArea textarea {
        background-color: #F1F1F1;
        color: #68bdb2;
    }
    .stSpinner {
        color: #FFDC00;
    }
    </style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("Bayan")
st.write("Welcome To Bayan!")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Upload Audio", "Real-Time Speech-to-Text"])

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to recognize speech from audio using OpenAI Whisper
def transcribe_audio_with_whisper(file, language="ar"):
    try:
        response = openai.Audio.transcribe(
            model="whisper-1",
            file=file,
            language=language
        )
        return response['text']
    except Exception as e:
        return f"Error: {str(e)}"

# Upload audio page
if page == "Upload Audio":
    uploaded_file = st.file_uploader("Upload an audio file or use real-time recording to start.", type=["wav", "mp3", "m4a"])
    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/wav")
        with st.spinner("Transcribing..."):
            transcript = transcribe_audio_with_whisper(uploaded_file)
            st.write("Here is the transcribed text:")
            st.text_area("Transcript", transcript, height=250)

# Real-Time Speech-to-Text page
elif page == "Real-Time Speech-to-Text":
    st.header("Real-Time Speech-to-Text (Bayan)")

    try:
        # Use st_audiorec for real-time audio recording
        audio_data = st_audiorec()

        if audio_data is not None:
            with st.spinner('Processing audio recording...'):
                # Play the recorded audio
                st.audio(audio_data, format='audio/wav')

                st.write("Transcribing...")
                # Transcribe the audio using OpenAI Whisper
                audio_bytes_io = BytesIO(audio_data)
                audio_bytes_io.name = 'audio.wav'  # Assign a name attribute
                transcript = transcribe_audio_with_whisper(audio_bytes_io)

                # Display the transcript
                st.write("Transcribed Text:")
                st.text_area("Transcript", transcript, height=200)
        else:
            st.write("Please record audio to get started.")

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

# Footer on both pages
st.sidebar.markdown("""
**Bayan**: A speech-to-text software designed for the Arabic language using OpenAI Whisper.
Bringing clarity to communication through Arabic Speech-to-Text.
""")
