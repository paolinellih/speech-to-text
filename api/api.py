from fastapi import FastAPI, UploadFile
from api.routes import users
from speech_to_text.transcribe import transcribe_audio

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])

@app.post("/speech-to-text")
async def speech_to_text(file: UploadFile):
    # Await the transcription process properly
    text = await transcribe_audio(file)
    return {"text": text}
