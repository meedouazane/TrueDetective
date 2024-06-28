#!/usr/bin/python3
"""
Speech to text module
"""
import requests
from pytube import YouTube
import os
from fpdf import FPDF
from Result2pdf import header_translate, text_writer
from tqdm import tqdm
from bs4 import BeautifulSoup


def get_title(url):
    """
    get the title of the video from YouTube url
    """
    r = requests.get(url)
    s = BeautifulSoup(r.text, "html.parser")
    title = str(s.title)
    title = title.replace('<title>', '').replace('- YouTube</title>', '')
    return title


def extract_audio_from_youtube(url):
    """
    Extracting audio from YouTube videos
    :param url: url of the video
    :return: the path of audio file
    """

    def progress_callback(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        progress.update(len(chunk))

    yt = YouTube(url, on_progress_callback=progress_callback)
    stream = yt.streams.filter(only_audio=True).first()

    # Ensure the directory exists
    os.makedirs('./tmp_Audio', exist_ok=True)

    # Generate random name for audio file
    #title = get_title(url)
    filename = 'myAudio.mp3'

    # Initialize tqdm progress bar
    with tqdm(total=stream.filesize,
              unit='B', unit_scale=True,
              desc=filename) as progress:
        file_path = stream.download(filename=f'./tmp_Audio/{filename}')
    return file_path


def speech_to_text(files, language=None, translate=False):
    default_lang = ""
    if language:
        default_lang = language
    token = os.environ.get('LEMONFOX_TOKEN')
    url = "https://api.lemonfox.ai/v1/audio/transcriptions"
    headers = {
        "Authorization": token
    }
    data = {
        "file": "https://output.lemonfox.ai/wikipedia_ai.mp3",
        "language": default_lang,
        "translate": translate,
        "response_format": "text"
    }
    filename = 'translation'
    #suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    #filename = "_".join([name, suffix])
    response = requests.post(url, headers=headers, files=files, data=data)
    if translate:
        # Ensure the directory exists
        os.makedirs('./tmp_Result', exist_ok=True)
        pdf = FPDF('P', 'mm', 'Letter')

        with open(f'./tmp_Result/{filename}', 'w') as f:
            f.write(response.json())
        header_translate(pdf)
        text_writer(pdf, f'./tmp_Result/{filename}')
        pdf.output(f'./tmp_Result/{filename}.pdf')
        print(f"PDF file of translation : ./tmp_Result/{filename}.pdf")
    return response.json()
