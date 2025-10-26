from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import time, os, jwt
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
SECRET = os.environ.get('INDERAI_JWT_SECRET','inderai-secret-sample')

# Simple in-memory "users" (for demo); in production use DB
USERS = {'admin': {'password': 'adminpass', 'role': 'superadmin'}, 'user': {'password':'userpass','role':'user'}}

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

@router.post('/token', response_model=Token)
def token(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    pwd = form_data.password
    user = USERS.get(username)
    if not user or user.get('password') != pwd:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    payload = {'sub': username, 'role': user.get('role'), 'iat': int(time.time())}
    tok = jwt.encode(payload, SECRET, algorithm='HS256')
    return {'access_token': tok, 'token_type': 'bearer'}

def verify_token(token: str):
    try:
        data = jwt.decode(token, SECRET, algorithms=['HS256'])
        return data
    except Exception as e:
        return None

def get_current_user(token: str = Depends(lambda: None)):
    # This function is a placeholder for dependency injection; in routers use your own extraction
    return None
