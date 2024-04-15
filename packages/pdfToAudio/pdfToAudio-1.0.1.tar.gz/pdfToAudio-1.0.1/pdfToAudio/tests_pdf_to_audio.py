import pytest
from unittest.mock import patch, MagicMock

from pdfToAudio.pdf_to_audio import pdf_to_audio

def test_pdf_to_audio():
    test_pdf_path = 'tsa.pdf'
    test_output_audio_path = 'output.mp3'
    test_lang = 'en'

    with patch('pdfToAudio.pdf_to_audio.PdfReader') as mock_pdf_reader, \
         patch('pdfToAudio.pdf_to_audio.gTTS') as mock_gtts:
        
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "This is test text."
        mock_pdf_reader.return_value.pages = [mock_page]
        
        pdf_to_audio(test_pdf_path, test_output_audio_path, test_lang)
        
        mock_gtts.assert_called_once_with(text="This is test text.", lang=test_lang)
        mock_gtts.return_value.save.assert_called_once_with(test_output_audio_path)

if __name__ == "__main__":
    pytest.main()
