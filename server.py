# server.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os
from process_pdf import process_pdf_to_audio

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # Save PDF
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process PDF → extract text → ElevenLabs → audio
    result = process_pdf_to_audio(file_path)

    return JSONResponse({
        "message": "PDF processed successfully",
        "pdf_path": file_path,
        "audio_path": result["audio_path"],
        "char_cost": result["char_cost"],
        "request_id": result["request_id"]
    })