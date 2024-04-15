from gtts import gTTS
from pypdf import PdfReader  

def pdf_to_audio(pdf_path, output_audio_path, lang):
    pdf_reader = PdfReader(pdf_path)
    full_text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

    tts = gTTS(text=full_text, lang=lang)
    tts.save(output_audio_path)
