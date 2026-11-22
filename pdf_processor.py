
import os
import sys

# Resilient PyMuPDF import with informative guidance if wrong python environment was invoked
try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf
    except ImportError as e:
        raise ImportError(
            "PyMuPDF is not installed in the currently running Python environment ("
            f"{sys.executable}). "
            "Please run this project using the virtual environment: .\\venv\\Scripts\\streamlit run app.py "
            "or use run_app.bat."
        ) from e

import pytesseract

from PIL import Image
from io import BytesIO

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Tesseract installation path check
tesseract_candidate = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.exists(tesseract_candidate):
    pytesseract.pytesseract.tesseract_cmd = tesseract_candidate


def load_and_split_pdf(pdf_path):

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    pdf = pymupdf.open(pdf_path)

    documents = []

    print("\n========== PDF EXTRACTION STARTED ==========")

    for page_index, page in enumerate(pdf):

        # Step 1: Extract selectable PDF text
        normal_text = page.get_text("text").strip()

        # Step 2: Convert page into an image
        pix = page.get_pixmap(
            matrix=pymupdf.Matrix(2, 2),
            alpha=False
        )

        image = Image.open(
            BytesIO(pix.tobytes("png"))
        )

        # Step 3: Extract text using OCR
        ocr_text = pytesseract.image_to_string(
            image,
            config="--psm 6"
        ).strip()

        # Step 4: Select the better extraction
        if len(ocr_text) > len(normal_text) * 1.2:
            final_text = ocr_text
            extraction_method = "OCR"
        else:
            final_text = normal_text
            extraction_method = "PDF Text"

        if not final_text:
            final_text = "[No readable text found]"

        # Step 5: Create document with page metadata
        document = Document(
            page_content=final_text,
            metadata={
                "source": pdf_path,
                "page": page_index,
                "page_label": str(page_index + 1),
                "extraction_method": extraction_method
            }
        )

        documents.append(document)

        print(
            f"Page {page_index + 1}: "
            f"{len(final_text)} characters "
            f"({extraction_method})"
        )

    pdf.close()

    # Step 6: Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = splitter.split_documents(documents)

    print("\n========== PDF PROCESSING RESULTS ==========")
    print(f"Total pages extracted: {len(documents)}")
    print(f"Total chunks created: {len(chunks)}")

    return documents, chunks


# Test the PDF processor independently
if __name__ == "__main__":

    pdf_path = "data/sample.pdf"

    pages, chunks = load_and_split_pdf(pdf_path)

    print("\n========== SAMPLE PAGE CONTENT ==========")

    for page_number in [12, 13, 14, 15]:
        if page_number < len(pages):
            print(f"\nPage {page_number + 1}:")
            print(pages[page_number].page_content)

    print("\n========== PDF PROCESSING SUCCESSFUL ==========")
