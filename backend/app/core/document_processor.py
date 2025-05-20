import os
import pytesseract
from PIL import Image
import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
import cv2 # OpenCV for image pre-processing if needed

# Configure Tesseract path if not in PATH (example for Windows)
# try:
#     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# except Exception:
    # pass # Silently pass if not on Windows or Tesseract is in PATH

def ocr_image(image_path: str) -> str:
    """Performs OCR on an image file."""
    try:
        # Optional: Image pre-processing using OpenCV can improve OCR
        # img = cv2.imread(image_path)
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # # Apply thresholding or other filters
        # _, processed_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # return pytesseract.image_to_string(Image.fromarray(processed_img))
        return pytesseract.image_to_string(Image.open(image_path))
    except Exception as e:
        print(f"Error during OCR for {image_path}: {e}")
        return ""

def extract_text_from_pdf(pdf_path: str) -> list:
    """Extracts text from a PDF file, page by page."""
    pages_content = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    pages_content.append((text, i + 1)) # Store text and page number (1-indexed)
    except Exception as e:
        print(f"Error extracting text from PDF {pdf_path}: {e}")
    return pages_content

def process_document(file_path: str, doc_id: str) -> list:
    """Processes a document (PDF or image) and extracts text."""
    _, file_extension = os.path.splitext(file_path.lower())
    pages_content = [] # List of (text, page_number)

    if file_extension == ".pdf":
        pages_content = extract_text_from_pdf(file_path)
    elif file_extension in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
        text = ocr_image(file_path)
        if text:
            pages_content.append((text, 1)) # Images are treated as single page
    else:
        print(f"Unsupported file type: {file_extension} for file {file_path}")
        # Optionally, raise an error or handle other text types (e.g., .txt, .docx)

    return pages_content

def get_document_text_chunks(text: str, doc_id: str, page_number: int, filename: str) -> list:
    """Splits text into chunks with metadata."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    
    chunk_list = []
    for i, chunk_text in enumerate(chunks):
        chunk_list.append({
            "text": chunk_text,
            "metadata": {"doc_id": doc_id, "page_number": page_number, "chunk_seq_id": i, "filename": filename}
        })
    return chunk_list