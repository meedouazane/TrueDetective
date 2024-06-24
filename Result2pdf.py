#!/usr/bin/python3
"""
Presentation of result in pdf file with specific header for each case
"""


def header_translate(pdf):
    """
    Header of translation results
    :param pdf: pdf file
    """
    pdf.add_page()
    pdf.image('./logo/translate_logo.jpg', 10, 7, 60)
    pdf.set_font("helvetica", "B", size=19)
    pdf.set_fill_color(230, 230, 0)
    pdf.set_text_color(255, 213, 0)
    pdf.cell(200, 27, txt='       Translation of The video',
             align='C', border=True, ln=True)
    pdf.ln(20)


def header_check(pdf):
    """
    Header of checking information results
    :param pdf: pdf file
    """
    pdf.add_page()
    pdf.image('./logo/fake_news_logo.jpeg', 10, 7, 60)
    pdf.set_font("helvetica", "B", size=19)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 27, txt='       Checking for false information',
             align='C', ln=True)
    pdf.ln(20)


def text_writer(pdf, file_path):
    """
    The body writer of the file
    """
    pdf.set_font("helvetica", size=12)
    pdf.set_text_color(0, 0, 0)
    with open(file_path, 'r', encoding='latin-1') as file:
        content = file.read()
    pdf.multi_cell(0, 10, content)
