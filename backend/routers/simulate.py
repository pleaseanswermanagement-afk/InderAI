from fastapi import APIRouter
from pydantic import BaseModel
import random
from ..data_utils import load_game_data

router = APIRouter()

class SimRequest(BaseModel):
    game: str
    compA: list
    compB: list
    iterations: int = 200

@router.post('/run')
def run_sim(req: SimRequest):
    data = load_game_data(req.game)
    def score(comp):
        s = 0
        for h in comp:
            for hh in data.get('heroes', []):
                if hh['name'].lower() == h.lower():
                    s += 10 + len(hh.get('notes',''))
            s += random.uniform(-5,5)
        return s
    wins = 0
    for _ in range(req.iterations):
        if score(req.compA) > score(req.compB):
            wins += 1
    return {'est_winrate_A': wins/req.iterations}
