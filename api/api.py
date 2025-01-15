from fastapi import FastAPI, UploadFile, Depends
from api.routes import users
from speech_to_text.transcribe import transcribe_audio
from api.utils.jwt_auth import get_current_user

app = FastAPI()

# Include the user-related routes
app.include_router(users.router, prefix="/users", tags=["users"])

@app.post("/speech-to-text", dependencies=[Depends(get_current_user)])
async def speech_to_text(file: UploadFile):
    """
    Transcribes audio to text. Access restricted to authenticated users.
    """
    # Transcribe the uploaded audio file
    text = await transcribe_audio(file)
    return {"text": text}

