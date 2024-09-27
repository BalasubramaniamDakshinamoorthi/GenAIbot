import io
import json
import os

import requests
import tqdm
from PyPDF2 import PdfReader


def download_and_parse_pdf(url: str) -> str:
    """
    Downloads a PDF file from the given URL and extracts the text content.

    Args:
    url (str): The URL of the PDF file to be downloaded and parsed.

    Returns:
    str: The extracted text content of the PDF file.
    """
    # Download the PDF file from the url
    info("downloading pdf")
    ic(url)
    response = requests.get(url)
    # Open the downloaded PDF file as a binary file
    pdf_file = io.BytesIO(response.content)
    # Create a PDF file reader object
    pdf_reader = PdfReader(pdf_file)
    # Initialize an empty string for the text
    text = ""
    info("parsing pdf")
    # Loop through each page in the PDF and extract the text
    for page_num in tqdm.tqdm(pdf_reader.pages):
        # page = pdf_reader.getPage(page_num)
        text += page_num.extract_text()
    # Return the extracted text
    return text


def parse_local(filename: str) -> str:
    """
    Extracts text from a local PDF file.

    Args:
    filename (str): The path to the local PDF file.

    Returns:
    str: The extracted text from the PDF file.
    """
    pdf_reader = PdfReader(filename)
    # Initialize an empty string for the text
    text = ""
    info("parsing pdf")
    # Loop through each page in the PDF and extract the text
    for page_num in tqdm.tqdm(pdf_reader.pages):
        # page = pdf_reader.getPage(page_num)
        text += page_num.extract_text()
    # Return the extracted text
    return text


# TODO: update to pydantic in the long term future
def parse_source(source: dict) -> dict:
    """
    Parse a source dictionary and extract relevant information.

    Args:
        source (dict): A dictionary containing source information.
            The dictionary should have the following keys:
            - 'title': The title of the source.
            - 'doc_format': The format of the source document (e.g., 'pdf').
            - 'url': The URL of the source document (if applicable).
            - 'local': A boolean indicating whether the source is a local file.
            - 'file': The path to the local file (if 'local' is True).

    Returns:
        dict: A dictionary containing the parsed source information.
            The dictionary will have the following keys:
            - 'title': The title of the source.
            - 'text': The extracted text content of the source document.
            If the source format is unknown, None is returned.
    """
    parsed_result = {k: v for k, v in source.items()}
    title = parsed_result["title"]
    doc_format = parsed_result.pop("doc_format")
    url = parsed_result.pop("url")
    local = parsed_result.pop("local")
    info("parsing source:")
    ic(title)
    ic(doc_format)
    ic(url)
    ic(local)
    if doc_format == "pdf" and local != True:
        assert doc_format == url.split(".")[-1]
        parsed_result["text"] = download_and_parse_pdf(url)
        return parsed_result
    elif doc_format == "pdf" and local == True:
        parsed_result["text"] = parse_local(parsed_result["file"])
        return parsed_result
    else:
        logger.warn(f"Unknown document format {doc_format}")
        return None
