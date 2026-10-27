"""All settings in one place so they are easy to find and tweak."""
from dotenv import load_dotenv

load_dotenv()  # reads OPENAI_API_KEY from the .env file

PDF_DIR = "data"              # put the mentor's PDFs here
CHROMA_DIR = "chroma_db"      # Chroma saves its database in this folder
COLLECTION_NAME = "pdf_docs"

EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"

CHUNK_SIZE = 800              # max characters per chunk (approx.)
CHUNK_OVERLAP = 150           # characters shared between neighbouring chunks
TOP_K = 3                     # how many chunks we retrieve and cite                   # how many chunks we retrieve and cite
 