from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.security import APIKeyHeader
from typing import List
import os
from dotenv import load_dotenv
from deepface import DeepFace
import tempfile

app = FastAPI()

# .envファイルから環境変数を読み込む（開発環境用）
load_dotenv()

# 環境変数からAPIキーを取得
API_KEY = os.getenv("FACE_AUTH_KEY")
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME)

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/compare_faces")
async def compare_faces(
    account: str = Form(...),
    files: List[UploadFile] = File(...),
    api_key: str = Depends(verify_api_key)
):
    if len(files) != 2:
        raise HTTPException(status_code=400, detail="Exactly two image files are required.")
    
    try:
        # 一時ファイルに画像を保存
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp1:
            temp1.write(await files[0].read())
            temp1_path = temp1.name
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp2:
            temp2.write(await files[1].read())
            temp2_path = temp2.name
        
        # DeepFaceのverify関数を呼び出し、結果を取得
        result = DeepFace.verify(
            img1_path=temp1_path,
            img2_path=temp2_path
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing images with DeepFace: {e}")
    finally:
        # 一時ファイルを削除
        os.remove(temp1_path)
        os.remove(temp2_path)

    measure_results = {
        'account': account,                             # アカウント名
        'distances': result['distance'],                # 顔の特徴量差分
        'identification': result['verified']            # 判定結果
    }

    return measure_results


