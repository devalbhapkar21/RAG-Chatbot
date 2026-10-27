"""Step 2: cut page text into small overlapping chunks.
 
Strategy (explained in README):
  * chunk each PAGE separately -> every chunk has an exact page number
  * split on paragraph/sentence boundaries first -> chunks read naturally
  * ~800 chars per chunk with 150 chars overlap -> context isn't lost at edges
"""
import re
from config import CHUNK_SIZE, CHUNK_OVERLAP
 
 
def split_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    #  break into paragraphs, and tidy up whitespace inside each one
    paragraphs = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", text)]
    paragraphs = [p for p in paragraphs if p]
 
    #  a paragraph longer than `size` is cut at a sentence end if possible
    pieces = []
    for p in paragraphs:
        while len(p) > size:
            cut = p.rfind(". ", 0, size)
            cut = cut + 1 if cut > size // 2 else size
            pieces.append(p[:cut].strip())
            p = p[cut:].strip()
        if p:
            pieces.append(p)
 
    #  pack pieces together until the chunk is full, then start a new one
    #   that begins with the tail of the previous chunk (the overlap)
    chunks, current = [], ""
    for piece in pieces:
        if current and len(current) + len(piece) + 1 > size:
            chunks.append(current)
            tail = current[-overlap:]
            tail = tail[tail.find(" ") + 1:]  # don't start mid-word
            current = f"{tail} {piece}"
        else:
            current = f"{current} {piece}".strip()
    if current:
        chunks.append(current)
    return chunks
 
 
def chunk_pages(pages):
    """Turn pages into chunk dicts that carry their source info (metadata)."""
    chunks = []
    for page in pages:
        for i, text in enumerate(split_text(page["text"])):
            chunks.append({
                "id": f"{page['doc']}::p{page['page']}::c{i}",  # unique + stable
                "text": text,
                "doc": page["doc"],
                "page": page["page"],
                "chunk_index": i,
            })
    return chunks
 