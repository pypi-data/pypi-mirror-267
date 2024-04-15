# PDF to Audio Converter

Convert PDF documents to spoken audio files using Google's Text-to-Speech service through the gTTS library and PyPDF2 for reading PDFs. This tool is ideal for creating audiobooks or for enhancing accessibility.


## Features
* Convert PDFs to audio: Turn any PDF document into an audio file.
* Multi-language support: Uses Google's Text-to-Speech which supports various languages.


## Installation
Install from PyPI with pip:

```bash
pip install pdfToAudio
```
## Quick Start


Here is how you can use the pdf_to_audio function to convert a PDF document into an audio file:


```bash
from pdfToAudio.pdf_to_audio import pdf_to_audio

pdf_path = 'path/to/your/pdf_file.pdf'

output_audio_path = 'path/to/your/audio_file.mp3'
language = 'en'  

pdf_to_audio(pdf_path, output_audio_path, language)
```


# License
This project is licensed under the MIT License - see the LICENSE file for details.



