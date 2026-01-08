from fastapi import FastAPI, UploadFile, File
import shutil

app = FastAPI()

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    file_location = f"uploads/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "PDF uploaded", "path": file_location}