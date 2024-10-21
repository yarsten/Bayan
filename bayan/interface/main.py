import streamlit as st
from PIL import Image
import openai  # type: ignore
import tempfile
import os

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

    /* Title Style */
    h1 {
        color: #68bdb2;  /* Updated title color */
        font-size: 42px;
        text-align: center;  /* Center the title */
    }

    /* Control Positioning */
    .stTextArea textarea {
        background-color: #F1F1F1;
        color: #111111;
        width: 100%;  /* Full width */
        height: 250px;  /* Height for the text area */
        margin: auto;  /* Center horizontally */
        display: block;  /* Ensure it behaves like a block element */
    }

    /* Style the file uploader */
    .stFileUploader {
        margin: 20px auto;  /* Center the file uploader */
        display: flex;
        flex-direction: column;  /* Stack elements vertically */
        align-items: center;  /* Center items */
    }

    /* Spinner Style */
    .stSpinner {
        color: #FFDC00;
    }

    /* Footer Style */
    footer {
        text-align: center;  /* Center footer text */
        color: white;  /* Footer text color */
        padding: 20px 0;  /* Padding for spacing */
    }
    </style>
""", unsafe_allow_html=True)

# Title and introduction with colors matching Bayan theme
st.title("Bayan: Arabic Speech-to-Text")
st.write("**Welcome to Bayan**")
st.write("A speech-to-text software designed for the Arabic language.")

# Session state to track whether the user is on the start page or upload page
if 'start_page' not in st.session_state:
    st.session_state.start_page = True

# Start page content
if st.session_state.start_page:
    if st.button("Start"):
        st.session_state.start_page = False  # Move to upload page

# Upload audio file page
if not st.session_state.start_page:
    st.write("Upload an audio file below to start.")  # Instruction

    # Upload audio file
    uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3"])

    # Set your OpenAI API key directly (use environment variable or secret management in production)
    openai.api_key = ""  # Direct assignment for testing only

    # Function to transcribe audio using OpenAI's Whisper
    def transcribe_audio(file):
        # Create a temporary file to save the uploaded audio
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
            temp_audio_file.write(file.read())
            temp_audio_file.flush()

            # Call OpenAI's Whisper model for transcription
            try:
                with open(temp_audio_file.name, "rb") as audio_file:
                    response = openai.Audio.transcribe(
                        model="whisper-1",
                        file=audio_file,
                        language="ar"  # Language code for Arabic
                    )
                    return response['text']  # Extract the transcription text
            except Exception as e:
                return f"Error during transcription: {str(e)}"
            finally:
                os.remove(temp_audio_file.name)  # Clean up the temporary file

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
