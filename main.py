import os
import sys
 
from config import PDF_DIR
from loader import load_pdfs
from chunker import chunk_pages
from store import add_chunks, get_collection
from qa import answer_question
 
 
def ingest():
    print("Reading PDFs...")
    pages = load_pdfs(PDF_DIR)
    chunks = chunk_pages(pages)
    print(f"Created {len(chunks)} chunks from {len(pages)} pages. Embedding...")
    total = add_chunks(chunks, reset=True)
    print(f"Done. Database holds {total} chunks.\n")
 
 
def show(question):
    result = answer_question(question)
    print("\nANSWER:\n" + result["answer"])
    print("\nTOP SOURCES:")
    for i, s in enumerate(result["sources"], start=1):
        snippet = s["text"][:200].replace("\n", " ")
        print(f"  [{i}] {s['doc']} | page {s['page']} | chunk {s['chunk_index']}"
              f" | similarity {s['score']}")
        print(f"      \"{snippet}...\"")
    print()
 
 
def run_tests(path="questions.txt"):
    with open(path, encoding="utf-8") as f:
        questions = [line.strip() for line in f if line.strip()]
    for n, q in enumerate(questions, start=1):
        print("=" * 70 + f"\nQ{n}: {q}")
        show(q)
 
 
def main():
    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY not set. Copy .env.example to .env and add your key.")
 
    if get_collection().count() == 0:  # first run: build the database
        ingest()
 
    print("Ask a question about your PDFs (type 'exit' to quit, 'test' to run questions.txt)")
    while True:
        question = input("\n> ").strip()
        if not question:
            continue
        if question.lower() == "exit":
            break
        elif question.lower() == "ingest":
            ingest()
        elif question.lower() == "test":
            run_tests()
        else:
            show(question)
 
 
if __name__ == "__main__":
    main()
 