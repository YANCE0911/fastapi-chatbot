import openai
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

# 環境変数の読み込み（.env の APIキーを取得）
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# ユーザーの入力を受け取るデータモデル
class ChatRequest(BaseModel):
    message: str

# ChatGPT APIを呼び出すエンドポイント（最新バージョン対応）
@app.post("/chat")
def chat_with_ai(request: ChatRequest):
    client = openai.OpenAI()  # 🔥 最新の `OpenAI` クラスを使う
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # モデル指定（GPT-4を使う場合は "gpt-4"）
        messages=[{"role": "user", "content": request.message}]
    )
    return {"response": response.choices[0].message.content}
