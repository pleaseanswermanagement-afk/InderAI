from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
import os, json, shutil

router = APIRouter()
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

class GameModule(BaseModel):
    game: str
    payload: dict

@router.post('/upload_module')
def upload_module(m: GameModule, authorization: str = None):
        # Authorization header expected: 'Bearer <token>'
        if authorization:
            token = authorization.split(' ')[1] if ' ' in authorization else authorization
            from ..routers.auth import verify_token
            info = verify_token(token)
            if not info or info.get('role') != 'superadmin':
                raise HTTPException(status_code=403, detail='Forbidden')

    gdir = os.path.join(DATA_DIR, m.game.lower())
    os.makedirs(gdir, exist_ok=True)
    p = os.path.join(gdir, 'meta.json')
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(m.payload, f, indent=2)
    return {'status':'ok', 'path': p}

@router.post('/upload_file')
async def upload_file(game: str = Form(...), file: UploadFile = File(...), authorization: str = None):
        if authorization:
            token = authorization.split(' ')[1] if ' ' in authorization else authorization
            from ..routers.auth import verify_token
            info = verify_token(token)
            if not info or info.get('role') not in ['superadmin','admin']:
                raise HTTPException(status_code=403, detail='Forbidden')

    gdir = os.path.join(DATA_DIR, game.lower())
    os.makedirs(gdir, exist_ok=True)
    dest = os.path.join(gdir, file.filename)
    with open(dest, 'wb') as fh:
        fh.write(await file.read())
    return {'status':'ok', 'path': dest}

@router.get('/list_modules')
def list_modules(authorization: str = None):
        # allow listing for authenticated users but optional for demo
        if authorization:
            token = authorization.split(' ')[1] if ' ' in authorization else authorization
            from ..routers.auth import verify_token
            info = verify_token(token)
            if not info:
                raise HTTPException(status_code=401, detail='Invalid token')

    items = []
    for d in os.listdir(DATA_DIR):
        items.append(d)
    return {'modules': items}

@router.post('/rebuild_index')
def rebuild_index(authorization: str = None):
        if authorization:
            token = authorization.split(' ')[1] if ' ' in authorization else authorization
            from ..routers.auth import verify_token
            info = verify_token(token)
            if not info or info.get('role') not in ['superadmin','admin']:
                raise HTTPException(status_code=403, detail='Forbidden')

    # trigger retriever build endpoint by calling its function (simple import)
    from ..retriever.faiss_wrapper import _build_index
    idx, docs = _build_index()
    return {'built': bool(idx is not None), 'docs_count': len(docs) if docs else 0}
