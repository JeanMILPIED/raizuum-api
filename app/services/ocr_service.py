import os
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from fastapi import UploadFile
import tempfile


def extract_text_by_page(pdf_path):
    """
    Extract text from a PDF file, returning a list of strings where each string is the text of a single page.

    :param pdf_path: Path to the PDF file.
    :return: List of strings, each representing the text of a page.
    """
    pages_text = []

    for page_layout in extract_pages(pdf_path):
        page_text = ""
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                page_text += element.get_text()
        pages_text.append(page_text)

    return pages_text


async def process_pdf(file: UploadFile):
    """
    Handles an uploaded PDF, extracts text, and returns structured data.

    :param file: UploadedFile from FastAPI.
    :return: Extracted text as a list of pages.
    """
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(await file.read())
        tmp_pdf_path = tmp_file.name

    # Extract text
    text_pages = extract_text_by_page(tmp_pdf_path)

    # Delete temporary file after processing
    os.remove(tmp_pdf_path)

    return text_pages
