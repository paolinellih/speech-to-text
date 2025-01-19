# import speech_recognition as sr
# from fastapi import UploadFile
# import os

# async def transcribe_audio(file: UploadFile):
#     # Save uploaded file temporarily
#     temp_file = f"temp_{file.filename}"
#     with open(temp_file, "wb") as f:
#         f.write(await file.read())

#     # Transcribe the audio
#     recognizer = sr.Recognizer()
#     with sr.AudioFile(temp_file) as source:
#         audio_data = recognizer.record(source)
#         text = recognizer.recognize_google(audio_data)
    
#     # Clean up
#     os.remove(temp_file)
#     return text
