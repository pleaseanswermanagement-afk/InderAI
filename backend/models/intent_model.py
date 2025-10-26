from sentence_transformers import SentenceTransformer
import numpy as np
model = SentenceTransformer('all-MiniLM-L6-v2')

CANONICAL = {
    'draft_request': [
        'what should i pick',
        'recommend a hero',
        'who to pick'
    ],
    'in_game_advice': [
        'i am getting ganked',
        'how to rotate',
        'when to take objective'
    ],
    'simulate': [
        'simulate match',
        'what if i pick'
    ]
}

CAN_EMBS = {k: model.encode(v) for k, v in CANONICAL.items()}

def detect_intent(text: str):
    t = text.strip().lower()
    emb = model.encode([t])[0]
    best_intent = 'unknown'
    best_sim = -1.0
    for intent, embs in CAN_EMBS.items():
        sims = (embs @ emb) / (((embs**2).sum(axis=1)**0.5) * (((emb**2).sum())**0.5))
        m = float(sims.max())
        if m > best_sim:
            best_sim = m
            best_intent = intent
    if best_sim < 0.45:
        return 'unknown', float(best_sim)
    return best_intent, float(best_sim)
