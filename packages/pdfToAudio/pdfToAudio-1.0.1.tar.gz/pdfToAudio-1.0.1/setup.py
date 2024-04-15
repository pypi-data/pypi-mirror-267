from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='pdfToAudio',
    version='1.0.1',
    packages=find_packages(),
    description='This package creates audiobooks from PDF files',
    author='Thiago S Adriano',
    author_email='prof.thiagoadriano@gmail.com',
    install_requires=[
        'gTTS==2.2.3',
        'pypdf==2.4.0'
    ],
    url='https://github.com/programadriano/is-even',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown' 
)