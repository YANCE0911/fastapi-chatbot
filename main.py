import openai
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# FastAPIアプリを作成
app = FastAPI()

# ここでCORSを許可する
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番はここを自分のドメインにした方が安全
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 環境変数の読み込み（.env の APIキーを取得）
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# OpenAI APIクライアントを作成（1回だけ定義して使い回す）
client = openai.OpenAI()

# ユーザーの入力を受け取るデータモデル
class ChatRequest(BaseModel):
    message: str

# ChatGPT APIを呼び出すエンドポイント（最新バージョン対応）
@app.post("/chat")
def chat_with_ai(request: ChatRequest):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # モデル指定（GPT-4を使う場合は "gpt-4"）
        messages=[{"role": "user", "content": request.message}]
    )
    return {"response": response.choices[0].message.content}

# 再デプロイのためのコメント追加
