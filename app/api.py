from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage,AIMessage
from app.hr_assistant import process_query

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class QueryRequest(BaseModel):
    query: str
    chat_history: list[Message]

@app.post("/chat")
def chat(request: QueryRequest):
    formatted_history = []
    for msg in request.chat_history:
        if msg.role == "user":
            formatted_history.append(
                HumanMessage(content=msg.content)
            )
        elif msg.role == "assistant":
            formatted_history.append(
                AIMessage(content=msg.content)
            )
    response = process_query(
        request.query,
        formatted_history
    )
    return response

