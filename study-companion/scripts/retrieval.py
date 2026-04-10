import re
from rank_bm25 import BM25Okapi

def tokenize(text):
    return re.findall(r'\w+', text.lower())

def build_bm25_index(chunks):
    tokenized_chunks = [tokenize(chunk["text"]) for chunk in chunks]
    bm25 = BM25Okapi(tokenized_chunks)
    return bm25

def lexical_search(query, chunks, bm25, top_k=3):
    scores = bm25.get_scores(tokenize(query))
    ranked = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)

    hits = []
    for chunk, score in ranked:
        if score <= 0:
            continue
        hits.append({**chunk, "score": float(score)})
        if len(hits) >= top_k:
            break

    return hits

