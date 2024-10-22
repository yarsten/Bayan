import os
import streamlit as st
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from io import BytesIO
from PIL import Image
import openai

# Load and display the logo at the top of the app
logo = Image.open("/home/yara/code/yarsten/Bayan/bayan/interface/image/Bayan_Interface_tp.png")  # Replace with the path to your logo file
st.image(logo, width=400)  # Adjust the width as needed

# Custom CSS for styling to match the Bayan PDF
st.markdown("""
    <style>
    body {
        background-color: #001f3f;
    }
    .css-18e3th9 {
        background-color: #001f3f;
    }
    .css-1d391kg p, .css-1d391kg div {
        color: #FFFFFF;
        font-size: 18px;
    }
    .css-10trblm {
        background-color: #FFFFFF;
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
    .css-15tx938, .css-qbe2hs {
        color: #FFFFFF;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("Bayan")
st.write("Welcome To Bayan!")

# Sidebar for navigation between two pages
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Upload Audio", "Real-Time Speech-to-Text"])

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to recognize speech from audio using OpenAI Whisper
def transcribe_audio_with_whisper(file, language="ar"):
    try:
        # Call Whisper model
        response = openai.Audio.transcribe(
            model="whisper-1",
            file=file,
            language=language
        )
        transcript = response['text']
        return transcript
    except Exception as e:
        return f"Error: {str(e)}"

# Upload audio page
if page == "Upload Audio":
    # Upload audio file
    uploaded_file = st.file_uploader("Upload an audio file or use real-time recording to start.", type=["wav", "mp3", "m4a"])

    # If the user uploads an audio file
    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/wav")

        # Process the audio file
        with st.spinner("Transcribing..."):
            transcript = transcribe_audio_with_whisper(uploaded_file)
            st.write("Here is the transcribed text:")
            st.text_area("Transcript", transcript, height=250)

# Real-Time Speech-to-Text page
elif page == "Real-Time Speech-to-Text":
    st.header("Real-Time Speech-to-Text (Bayan)")

    # Constants for audio recording
    SAMPLE_RATE = 16000  # 16kHz for Speech-to-Text
    DURATION = 5  # Record 5 seconds of audio

    try:
        # Check if an input device is available
        devices = sd.query_devices(kind='input')
        if devices:
            # Function to record audio in real-time
            def record_audio(duration, sample_rate):
                st.write("Recording... Speak now!")
                audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
                sd.wait()  # Wait until the recording is finished
                return audio

            # Function to save NumPy audio as a WAV file for Whisper
            def audio_to_wav_bytes(audio, sample_rate):
                wav_io = BytesIO()
                wav.write(wav_io, sample_rate, audio)
                wav_io.seek(0)  # Move pointer to the beginning of the file
                return wav_io

            # Automatically record audio and transcribe as soon as the page is loaded
            with st.spinner("Recording... Speak now for 5 seconds"):
                audio_np = record_audio(DURATION, SAMPLE_RATE)

            st.write("Recording finished! Transcribing...")

            # Convert recorded audio to WAV format and transcribe with Whisper
            audio_wav_io = audio_to_wav_bytes(audio_np, SAMPLE_RATE)
            transcript = transcribe_audio_with_whisper(audio_wav_io)

            # Display the transcript
            st.write("Transcribed Text:")
            st.text_area("Transcript", transcript, height=200)

        else:
            st.error("No audio input devices found. Please connect a microphone.")

    except sd.PortAudioError as e:
        st.error(f"An error occurred while querying audio devices: {str(e)}. Please check your microphone settings.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

# Footer on both pages
st.sidebar.markdown("""
**Bayan**: A speech-to-text software designed for the Arabic language using OpenAI Whisper.
Bringing clarity to communication through Arabic Speech-to-Text.
""")
