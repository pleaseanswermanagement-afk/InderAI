# LLM wrapper: tries OpenAI if API key present, else uses a local heuristic stub.
import os, json
import requests

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')

def call_openai(prompt, max_tokens=256, temperature=0.3):
    if not OPENAI_KEY:
        raise RuntimeError('OPENAI_API_KEY not set')
    import openai
    openai.api_key = OPENAI_KEY
    resp = openai.ChatCompletion.create(
        model='gpt-4o-mini', # placeholder — change as needed
        messages=[{'role':'system','content':'You are InderAI, a game strategy assistant.'},
                  {'role':'user','content': prompt}],
        max_tokens=max_tokens,
        temperature=temperature
    )
    return resp['choices'][0]['message']['content']

def generate_response(prompt, max_tokens=256):
    try:
        if OPENAI_KEY:
            return call_openai(prompt, max_tokens=max_tokens)
    except Exception as e:
        # fallthrough to local stub
        pass
    # Local stub: echo prompt with simple heuristics
    if 'draft' in prompt.lower() or 'pick' in prompt.lower():
        return 'LocalStub: pick hero X for synergy; pick priority 1-3.'
    if 'simulate' in prompt.lower():
        return 'LocalStub: simulation suggests comp A has 52% winrate.'
    return 'LocalStub: sorry, I could not call an LLM. Provide OPENAI_API_KEY to enable.'
