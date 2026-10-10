**AI Marketing Copilot**

An Agentic AI marketing assistant built with Python, LangGraph, RAG, MCP, FastAPI, and Qwen3/Ollama.

It analyzes marketing requests, selects relevant tools, retrieves product and customer context, generates campaigns, and validates the output.

 **Features**

- Agentic AI workflow with LangGraph
- Local Qwen3 LLM using Ollama
- RAG with Sentence Transformers and vector search
- MCP client-server tool architecture
- Customer segmentation with SQLite
- Campaign validation and retry
- REST API using FastAPI
- Automated testing with Pytest

 **Tech Stack**

Python · LangGraph · Qwen3 · Ollama · RAG · MCP · FastAPI · SQLite · Sentence Transformers · Pytest · Git

 **Architecture**

```mermaid
flowchart TD
    A[User Request] --> B[FastAPI]
    B --> C[LangGraph Agent]
    C --> D[Intent Classification]
    D --> E[Tool Selection]
    E --> F[MCP Client]
    F --> G[MCP Server]

    G --> H[Product Tool]
    G --> I[Customer Tool]
    G --> J[Marketing Tool]

    H --> K[RAG Product Knowledge]
    I --> L[SQLite Customer Data]
    J --> M[RAG Marketing Guidelines]

    K --> N[Retrieved Context]
    L --> N
    M --> N

    N --> O[Qwen3 Ollama]
    O --> P[Campaign Generation]
    P --> Q[Campaign Validator]

    Q -->|Valid| R[Final Marketing Campaign]
    Q -->|Invalid| O
```

 **Run Locally**

**cmd**

git clone https://github.com/JafsinJaleel/marketing-copilot.git

cd marketing-copilot

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

ollama pull qwen3:4b

uvicorn app.api.main:app --reload


API: `http://127.0.0.1:8000`

Swagger: `http://127.0.0.1:8000/docs`

**Testing**
**cmd**

pytest -q

