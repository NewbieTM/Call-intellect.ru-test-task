import os
from docx import Document

def save_text_to_docx(text, filename):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(filename)

def save_text_to_txt(text, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)

def create_output_directory():
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
