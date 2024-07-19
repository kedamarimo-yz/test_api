""" from fastapi import FastAPI
from pydantic import BaseModel

class Data(BaseModel):
    x: int
    y: int

app = FastAPI()

@app.get('/')
def index():
    return {'message': 'Hello!'}

@app.post('/calc')
def face_recognition(data: Data):
    z = data.x*data.y
    return {'result': z} """
    
    
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む（開発環境用）
load_dotenv()

# 環境変数からAPIキーを取得
API_KEY = os.getenv("FACE_AUTH_KEY")
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME)

app = FastAPI()

def get_api_key(api_key: str = Depends(api_key_header)):
    print('API_KEY: ')
    print(str(API_KEY))
    print('api_key: ')
    print(str(api_key))
    if api_key != API_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    return api_key

@app.get("/")
def read_root(api_key: str = Depends(get_api_key)):
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None, api_key: str = Depends(get_api_key)):
    return {"item_id": item_id, "q": q}
