from fastapi import FastAPI
from pydantic import BaseModel

from app.agents.agentic_campaign import agent


app = FastAPI(
    title="AI Marketing Copilot",
    description="Agentic AI marketing assistant powered by LangGraph, RAG, MCP, and Qwen3.",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    message: str
    intent: str
    response: str
    validation_status: str
    retry_count: int


@app.get("/")
def root():
    return {
        "name": "AI Marketing Copilot",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    initial_state = {
        "message": request.message,

        "intent": "",

        "use_product_tool": False,
        "use_customer_tool": False,
        "use_marketing_tool": False,

        "product_executed": False,
        "customer_executed": False,
        "marketing_executed": False,

        "product_context": "",
        "customer_context": "",
        "marketing_context": "",
        "combined_context": "",

        "response": "",
        "campaign": "",

        "validation_status": "",
        "validation_message": "",

        "retry_count": 0,
    }

    result = agent.invoke(initial_state)

    return ChatResponse(
        message=request.message,
        intent=result["intent"],
        response=result["response"],
        validation_status=result["validation_status"],
        retry_count=result["retry_count"],
    )