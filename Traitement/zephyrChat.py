#!/usr/bin/python3
"""
ZepherChat module to check given text
"""
from openai import OpenAI
import os
from fpdf import FPDF
from Result2pdf import header_check, text_writer


def check(content):
    """
    Extracting audio from YouTube videos and checking it
    for false information
    :param content: text that we'll check
    :return: result of checking
    """
    token = os.environ.get('LEMONFOX_TOKEN')
    client = OpenAI(
        api_key=token,
        base_url="https://api.lemonfox.ai/v1",
    )
    completion = client.chat.completions.create(
        messages=[
            {"role": "system",
             "content": "You are an AI trained to identify and verify "
                        "factual information. Please check the following "
                        "text for any false information and provide corrections "
                        "or confirmations."},
            {"role": "user", "content": content}
        ],
        model="zephyr-chat",
    )
    os.makedirs('./tmp_Result', exist_ok=True)
    pdf = FPDF('P', 'mm', 'Letter')
    filename = 'checking'
    #suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    #filename = "_".join([name, suffix])
    with open(f'./tmp_Result/{filename}', 'w') as f:
        f.write(completion.choices[0].message.content)
    header_check(pdf)
    text_writer(pdf, f'./tmp_Result/{filename}')
    pdf.output(f'./tmp_Result/{filename}.pdf')
    print(f"PDF file of Checking : tmp_Result/{filename}.pdf")
    return completion.choices[0].message.content
