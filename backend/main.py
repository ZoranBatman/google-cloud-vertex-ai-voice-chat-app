# uvicorn main:app
# uvicorn main:app --reload
# source venv/bin/activate


# Main imports
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from google.cloud import aiplatform
import librosa
#import soundfile as sf
import os


# Import custom functions
from functions.vertexai_requests import convert_audio_to_text, get_chat_response, reset_chat_history, memory
from functions.text_to_speech import convert_text_to_speech

# Initiate App
app = FastAPI()


# CORS - Origins
# From which domains requests will be accepted
origins = [
    "https://vertexai-voice-chat-frontend-odxwj2pgcq-ew.a.run.app"
]


# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Check Health API endpoint
@app.get("/")
async def check_health():
    return {"message": "healthy"}



# Reset Chat History
@app.get("/reset/")  # Or use a POST endpoint if preferred
async def reset_chat():  # We can make this async in case of future I/O needs
    reset_chat_history()
    return {"message": "Chat history reset successfully"}


# Post audio
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):

    
    # Save file from Frontend
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")
    audio_bytes = audio_input.read()

    
    # Decode Audio
    message_decoded = convert_audio_to_text(audio_bytes)
    print(message_decoded)
    

   #Guard: Ensure message decoded
    if not message_decoded: 
        return HTTPException(status_code=400, detail= "Failed to decode audio.")
    
    # Get VertexAI response chat
    chat_response = get_chat_response(message_decoded)
    print(chat_response)
    
    #Guard: Ensure response from VertexAI
    if not chat_response: 
        return HTTPException(status_code=400, detail= "Failed to get chat response.")
    
    # Convert chat response to audio
    audio_output = convert_text_to_speech(chat_response)

    #Guard: Ensure response from VertexAI
    if not audio_output: 
        return HTTPException(status_code=400, detail= "Failed to convert chat response to audio.")
    
    # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    # Return audio file
    return StreamingResponse(iterfile(), media_type="application/octet-stream")
    
    return "Done."