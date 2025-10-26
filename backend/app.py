from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import chat, draft, admin, simulate, retriever
app = FastAPI(title='InderAI Complete')

app.include_router(chat.router, prefix='/api/chat', tags=['chat'])
app.include_router(draft.router, prefix='/api/draft', tags=['draft'])
app.include_router(simulate.router, prefix='/api/simulate', tags=['simulate'])
app.include_router(admin.router, prefix='/api/admin', tags=['admin'])
app.include_router(retriever.router, prefix='/api/retriever', tags=['retriever'])

# serve frontend
app.mount('/', StaticFiles(directory='../frontend', html=True), name='frontend')

@app.get('/health')
def health():
    return {'status':'ok'}

from .monitoring.metrics import metrics_endpoint
@app.get('/metrics')
def metrics():
    return metrics_endpoint()
