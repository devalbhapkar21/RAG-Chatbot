from config import CHAT_MODEL, TOP_K
from store import get_openai, search
 
SYSTEM_PROMPT = (
    "You answer questions using ONLY the numbered context excerpts provided. "
    "Cite the excerpts you used like [1] or [2]. "
    "If the answer is not in the excerpts, say: "
    "\"I couldn't find that in the provided documents.\" Do not guess."
)
 
 
def answer_question(question, k=TOP_K):
    hits = search(question, k)
 
    context = "\n\n".join(
        f"[{i}] (source: {h['doc']}, page {h['page']})\n{h['text']}"
        for i, h in enumerate(hits, start=1)
    )
    response = get_openai().chat.completions.create(
        model=CHAT_MODEL,
        temperature=0,  # same question -> same answer, good for testing
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )
    return {"answer": response.choices[0].message.content.strip(), "sources": hits}