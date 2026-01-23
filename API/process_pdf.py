import os
import pdfplumber
from elevenlabs.client import ElevenLabs

API_KEY = os.environ.get("ELEVENLABS_API_KEY")
if not API_KEY:
    raise RuntimeError("ELEVENLABS_API_KEY not set in environment")

client = ElevenLabs(api_key=API_KEY)


def extract_text_from_pdf(pdf_path: str) -> str:
    texts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                texts.append(t)
    return "\n\n".join(texts)


def process_pdf_to_audio(pdf_path: str, voice_id: str = "voice_id", out_path: str | None = None):
    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        raise ValueError("No text extracted from PDF")

    response = client.text_to_speech.with_raw_response.convert(
        text=text,
        voice_id=voice_id
    )

    char_cost = None
    request_id = None
    try:
        char_cost = response.headers.get("x-character-count")
        request_id = response.headers.get("request-id")
    except Exception:
        pass

    if out_path is None:
        base = os.path.splitext(os.path.basename(pdf_path))[0]
        out_dir = os.path.dirname(pdf_path) or "."
        out_path = os.path.join(out_dir, f"{base}.mp3")

    with open(out_path, "wb") as f:
        f.write(response.data)

    return {"audio_path": out_path, "char_cost": char_cost, "request_id": request_id}