from fastapi.testclient import TestClient
from backend.app import app
client = TestClient(app)

def test_draft_suggest():
    res = client.post('/api/draft/suggest', json={'game':'mlbb','available':['Yu Zhong','Lesley']})
    assert res.status_code == 200
    j = res.json()
    assert 'recommendations' in j
