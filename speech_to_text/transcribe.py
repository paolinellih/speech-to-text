import speech_recognition as sr
from fastapi import UploadFile
import os
from pydub import AudioSegment
import tempfile
import time

async def transcribe_audio(file: UploadFile):
    # Create a unique name
    unique_filename = f"{int(time.time() * 1000)}"
    # Save uploaded file temporarily
    temp_file = f"temp_{unique_filename}"
    with open(temp_file, "wb") as f:
        f.write(await file.read())

    # Ensure ffmpeg is available
    try:
        audio = AudioSegment.from_file(temp_file)
    except Exception as e:
        os.remove(temp_file)
        return f"Error processing audio file"

    # Convert the file to WAV if it's not already in a supported format
    try:
        temp_wav = tempfile.mktemp(suffix=".wav")  # Create a temporary file with a .wav suffix
        audio.export(temp_wav, format="wav")
    except Exception as e:
        os.remove(temp_file)
        return f"Error converting audio file"

    # Transcribe the audio
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(temp_wav) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
    except Exception as e:
        os.remove(temp_file)
        os.remove(temp_wav)
        return f"Error transcribing audio file"

    # Clean up temporary files after transcription
    os.remove(temp_file)
    os.remove(temp_wav)

    return text
