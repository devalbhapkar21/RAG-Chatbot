
"""Step 1: read every PDF in a folder, page by page."""
from pathlib import Path
from pypdf import PdfReader
 
 
def load_pdfs(pdf_dir):
    """Return a list of {"doc", "page", "text"} - one entry per non-empty page."""
    pages = []
    pdf_files = sorted(Path(pdf_dir).glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in '{pdf_dir}/'")
 
    for pdf_path in pdf_files:
        try:
            reader = PdfReader(pdf_path)
        except Exception as e:  # a broken PDF should not stop the whole run
            print(f"  ! Skipping {pdf_path.name}: {e}")
            continue
 
        count = 0
        for page_number, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()
            if text:  # scanned/image-only pages give empty text
                pages.append({"doc": pdf_path.name, "page": page_number, "text": text})
                count += 1
        print(f"  Loaded {pdf_path.name}: {count} pages with text")
    return pages