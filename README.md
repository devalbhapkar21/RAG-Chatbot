# PDF RAG Pipeline (OpenAI + Chroma)

Ask natural-language questions about a folder of PDFs. The pipeline returns an
answer plus the **top 3 source chunks** (document name, page, chunk number, snippet).

```
PDFs -> extract text per page -> chunk -> embed (OpenAI) -> Chroma
Question -> embed -> top-3 similar chunks -> GPT answers from them -> answer + citations
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env          # then put your OPENAI_API_KEY inside
# copy the 5-10 PDFs into the data/ folder
```

## Usage

```bash
python main.py
```

* First run: it automatically reads every PDF in `data/` and builds the database.
* Then type your question at the `>` prompt and press Enter.
* Other commands at the prompt: `test` (runs all questions in `questions.txt`),
  `ingest` (rebuilds the database after you add/change PDFs), `exit` (quit).

## Project layout

| File | Job |
|---|---|
| `main.py` | The file you run; ingests on first run, then answers questions |
| `config.py` | Models and chunk settings in one place |
| `loader.py` | Reads all PDFs in `data/`, page by page |
| `chunker.py` | Splits page text into overlapping chunks |
| `store.py` | OpenAI embeddings + Chroma storage and search |
| `qa.py` | Retrieval + prompt + LLM answer |

## Chunking strategy (and why)

* **Chunk per page, never across pages.** This guarantees every chunk has an
  exact page number, which makes citations trustworthy. Trade-off: a sentence
  that straddles a page break is split in two; the overlap softens this only
  within a page, which I accepted for citation accuracy.
* **~800 characters (~150-200 words).** Big enough to hold a complete idea or
  a short paragraph, small enough that the embedding stays focused on one topic
  (very large chunks blur many topics into one vector and retrieve poorly).
* **150-character overlap (~19%).** Facts that sit at a chunk boundary still
  appear whole in at least one chunk.
* **Paragraph / sentence-aware splitting.** The splitter packs whole paragraphs
  and cuts long ones at sentence ends, so chunks don't end mid-sentence.
  This is the same idea as a "recursive character splitter" but written in ~25
  readable lines with no extra dependency.
* Values live in `config.py`; if retrieval looks poor on the test questions,
  try 500/100 (more precise) or 1200/200 (more context) and re-ingest with `--reset`.

## Other design choices

* `text-embedding-3-small` - cheap, good quality; `gpt-4o-mini` for answers.
* Cosine similarity in Chroma (`hnsw:space = cosine`); the score shown is `1 - distance`.
* `temperature=0` so results are reproducible.
* The prompt forces the model to answer only from the retrieved excerpts and say
  "I couldn't find that" otherwise, which reduces hallucination.

## Test results



| # | Question | Correct? | Notes |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

## Known limitations

* Scanned (image-only) PDFs have no extractable text; they would need OCR.
* Tables are flattened to plain text by `pypdf`.
* Pure vector search can miss exact keywords/IDs; hybrid search or a reranker would help.
