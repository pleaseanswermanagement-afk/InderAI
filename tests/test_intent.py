from backend.models.intent_model import detect_intent

def test_intent_draft():
    intent, conf = detect_intent('siapa yang bagus buat dipick?')
    assert intent in ['draft_request','unknown']
    assert isinstance(conf, float)
