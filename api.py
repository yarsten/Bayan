import os
import tempfile
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
import openai
import uvicorn

app = FastAPI()

# HTML for the upload page
HTML_CONTENT = """
<!DOCTYPE html>
<html>
    <head>
        <title>Bayan: Arabic Speech-to-Text</title>
    </head>
    <body>
        <h1>Upload Audio File for Transcription</h1>
        <form action="/transcribe" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".wav,.mp3,.m4a,.mp4">
            <input type="submit">
        </form>
    </body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def main():
    return HTML_CONTENT

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    # Check the file type
    allowed_content_types = [
        "audio/wav", "audio/x-wav",
        "audio/mpeg", "audio/mp3",
        "audio/x-m4a", "audio/m4a",
        "audio/mp4"
    ]

    if file.content_type not in allowed_content_types:
        raise HTTPException(status_code=400, detail=f"Invalid file type '{file.content_type}'. Please upload a .wav, .mp3, or .m4a file.")

    # Read the audio file content
    audio_data = await file.read()

    # Temporary file to store the audio data
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
        temp_audio_file.write(audio_data)
        temp_audio_file.flush()  

        # API key from environment variable
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            raise HTTPException(status_code=500, detail="OpenAI API key not set.")

        # Call Whisper model
        try:
            with open(temp_audio_file.name, "rb") as audio_file:
                response = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language="ar"
                )
                transcription = response['text']
                return {"transcription": transcription}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            # Clean the temporary file
            os.remove(temp_audio_file.name)

# Start the FastAPI server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
