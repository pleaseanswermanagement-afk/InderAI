import os, json, numpy as np
from sentence_transformers import SentenceTransformer
import faiss

MODEL_NAME = 'all-MiniLM-L6-v2'
model = SentenceTransformer(MODEL_NAME)

INDEX_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'faiss.index')
DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'faiss_docs.json')

def _build_index():
    docs = []
    for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), '..', 'data')):
        for f in files:
            if f.endswith('.json'):
                p = os.path.join(root, f)
                try:
                    with open(p, 'r', encoding='utf-8') as fh:
                        docs.append({'path': p, 'text': fh.read()})
                except:
                    pass
    texts = [d['text'] for d in docs]
    if not texts:
        return None, None
    embs = model.encode(texts)
    d = embs.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(np.array(embs).astype('float32'))
    with open(DOCS_PATH, 'w', encoding='utf-8') as fh:
        json.dump([d['path'] for d in docs], fh)
    faiss.write_index(index, INDEX_PATH)
    return index, [d['path'] for d in docs]

def _load_index():
    if os.path.exists(INDEX_PATH) and os.path.exists(DOCS_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(DOCS_PATH, 'r', encoding='utf-8') as fh:
            docs = json.load(fh)
        return index, docs
    else:
        return _build_index()

def retrieve_docs(query, top_k=3):
    try:
        index, docs = _load_index()
        if index is None:
            return []
        q_emb = model.encode([query]).astype('float32')
        D, I = index.search(q_emb, top_k)
        results = []
        for idx in I[0]:
            if idx < len(docs):
                p = docs[idx]
                try:
                    with open(p, 'r', encoding='utf-8') as fh:
                        results.append(fh.read()[:1000])
                except:
                    results.append('')
        return results
    except Exception as e:
        return []

from fastapi import APIRouter
router = APIRouter()
@router.get('/build')
def build():
    idx, docs = _build_index()
    return {'built': bool(idx is not None), 'docs': docs or []}

@router.get('/search')
def search(q: str, k: int = 3):
    return {'results': retrieve_docs(q, top_k=k)}
