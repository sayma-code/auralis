from elevenlabs.client import ElevenLabs
import pdfplumber

client = ElevenLabs(api_key="api")

# 1. Extract text from PDF
pdf_path = "uploads/myfile.pdf"
text = extract_text_from_pdf(pdf_path)

# 2. Convert to audio
response = client.text_to_speech.with_raw_response.convert(
    text=text,
    voice_id="voice_id"
)

# 3. Access metadata
char_cost = response.headers.get("x-character-count")
request_id = response.headers.get("request-id")

# 4. Save audio file
with open("output_audio.mp3", "wb") as f:
    f.write(response.data)