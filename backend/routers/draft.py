from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from ..data_utils import load_game_data
from ..llm.wrapper import generate_response

router = APIRouter()

class DraftRequest(BaseModel):
    game: str
    team_picks: List[str] = []
    opponent_picks: List[str] = []
    available: List[str] = []

@router.post('/suggest')
def suggest(d: DraftRequest):
    data = load_game_data(d.game)
    heroes = data.get('heroes', [])
    available_set = set([h.lower() for h in d.available])
    recs = []
    for h in heroes:
        if h['name'].lower() in available_set:
            recs.append({'name': h['name'], 'role': h.get('role',''), 'notes': h.get('notes','')})
    # ask LLM for explanation of top picks
    prompt = f"Suggest top 3 picks for game {d.game} given available {d.available} and opponent picks {d.opponent_picks}"
    explanation = generate_response(prompt)
    return {'recommendations': recs[:5], 'explanation': explanation}
