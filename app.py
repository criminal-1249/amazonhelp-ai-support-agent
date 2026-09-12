from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from agent import run_agent

app = FastAPI(title="Amazon Help AI Support Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from typing import Optional

class ChatRequest(BaseModel):
    message: Optional[str] = None


@app.get("/")
def health_check():
    return {"status": "Amazon Support Agent is running"}


@app.post("/chat")
def chat(message: Optional[str] = None, request: Optional[ChatRequest] = None):
    user_msg = message
    if not user_msg and request and request.message:
        user_msg = request.message
    if not user_msg:
        user_msg = ""
    result = run_agent(user_msg)
    return result