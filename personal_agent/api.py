from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .agent import PersonalAgent

app = FastAPI(title="Personal AI Agent", version="0.1.0")
agent = PersonalAgent()


class ChatRequest(BaseModel):
    message: str
    use_web: bool = False


class MemoryRequest(BaseModel):
    content: str


class IngestRequest(BaseModel):
    path: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest) -> dict[str, str]:
    try:
        return {"response": agent.respond(request.message, request.use_web)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/memory")
def remember(request: MemoryRequest) -> dict[str, str]:
    agent.memory.remember(request.content)
    return {"status": "remembered"}


@app.post("/documents/ingest")
def ingest(request: IngestRequest) -> dict[str, str]:
    try:
        return {"message": agent.ingest(request.path)}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
