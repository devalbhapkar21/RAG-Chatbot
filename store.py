import chromadb
from openai import OpenAI
from config import CHROMA_DIR, COLLECTION_NAME, EMBED_MODEL
 
_client = None
 
 
def get_openai():
    global _client
    if _client is None:
        _client = OpenAI()  # uses OPENAI_API_KEY from the environment
    return _client
 
 
def embed(texts):
    """Turn a list of strings into a list of vectors."""
    response = get_openai().embeddings.create(model=EMBED_MODEL, input=texts)
    return [item.embedding for item in response.data]
 
 
def get_collection(reset=False):
    db = chromadb.PersistentClient(path=CHROMA_DIR)
    if reset:
        try:
            db.delete_collection(COLLECTION_NAME)
        except Exception:
            pass  # nothing to delete the first time
    return db.get_or_create_collection(
        COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )
 
 
def add_chunks(chunks, reset=False, batch_size=100):
    collection = get_collection(reset=reset)
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]
        texts = [c["text"] for c in batch]
        collection.upsert(  # upsert = insert, or overwrite if the id exists
            ids=[c["id"] for c in batch],
            documents=texts,
            embeddings=embed(texts),
            metadatas=[
                {"doc": c["doc"], "page": c["page"], "chunk_index": c["chunk_index"]}
                for c in batch
            ],
        )
        print(f"  Stored {min(start + batch_size, len(chunks))}/{len(chunks)} chunks")
    return collection.count()
 
 
def search(query, k):
    """Return the k chunks most similar to the query."""
    collection = get_collection()
    result = collection.query(query_embeddings=embed([query]), n_results=k)
    hits = []
    for text, meta, dist in zip(
        result["documents"][0], result["metadatas"][0], result["distances"][0]
    ):
        hits.append({
            "text": text,
            "doc": meta["doc"],
            "page": meta["page"],
            "chunk_index": meta["chunk_index"],
            "score": round(1 - dist, 3),  # cosine similarity (higher = closer)
        })
    return hits