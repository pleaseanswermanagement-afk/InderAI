from fastapi import APIRouter
from pydantic import BaseModel
from ..models.intent_model import detect_intent
from ..retriever.faiss_wrapper import retrieve_docs
from ..llm.wrapper import generate_response

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str = None
    message: str

class ChatResponse(BaseModel):
    response_text: str
    intent: str
    confidence: float
    references: list = []

@router.post('/send', response_model=ChatResponse)
def send_message(req: ChatRequest):
    intent, confidence = detect_intent(req.message)
    docs = retrieve_docs(req.message, top_k=3)
    # build prompt
    prompt = f"""User message: {req.message}\n\nTop references:\n""" + '\n---\n'.join(docs)
    # call LLM wrapper (OpenAI or local stub)
    resp = generate_response(prompt)
    return ChatResponse(response_text=resp, intent=intent, confidence=confidence, references=docs)
