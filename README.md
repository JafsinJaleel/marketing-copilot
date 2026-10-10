Yes — for a GitHub portfolio, \*\*shorter is better\*\*. The README should quickly tell a recruiter \*\*what it is, what technologies you used, how it works, and how to run it\*\*.



I recommend this version:



````markdown

\# AI Marketing Copilot



An Agentic AI marketing assistant built with \*\*Python, LangGraph, RAG, MCP, FastAPI, and Qwen3/Ollama\*\*. It analyzes marketing requests, selects relevant tools, retrieves approved product and customer information, generates campaigns, and validates the output.



\## Key Features



\- \*\*Agentic AI\*\* workflow using LangGraph

\- \*\*LLM integration\*\* with local Qwen3 through Ollama

\- \*\*RAG pipeline\*\* using Sentence Transformers and vector similarity search

\- \*\*MCP client-server\*\* architecture for modular tool execution

\- \*\*Customer segmentation\*\* using SQLite

\- \*\*Dynamic tool selection\*\* for product, customer, and marketing data

\- \*\*Campaign validation and retry\*\* mechanism

\- \*\*FastAPI REST API\*\*

\- Automated testing with \*\*Pytest\*\*



\## Architecture



```text

User Request

&#x20;    ↓

FastAPI

&#x20;    ↓

LangGraph Agent

&#x20;    ↓

Intent Classification

&#x20;    ↓

Tool Selection

&#x20;    ↓

MCP Client → MCP Server

&#x20;    ↓

┌──────────────┬───────────────┬──────────────────┐

│ Product Tool │ Customer Tool │ Marketing Tool   │

└──────┬───────┴───────┬───────┴────────┬─────────┘

&#x20;      ↓                ↓                ↓

&#x20;     RAG            SQLite             RAG

&#x20;      └────────────────┼────────────────┘

&#x20;                       ↓

&#x20;                 Retrieved Context

&#x20;                       ↓

&#x20;                 Qwen3 / Ollama

&#x20;                       ↓

&#x20;               Campaign Generation

&#x20;                       ↓

&#x20;                   Validation

&#x20;                  ↙          ↘

&#x20;               Valid        Invalid

&#x20;                 ↓             ↓

&#x20;            Final Output     Retry

````



\## Tech Stack



| Category        | Technologies                                     |

| --------------- | ------------------------------------------------ |

| Language        | Python                                           |

| Agentic AI      | LangGraph                                        |

| LLM             | Qwen3, Ollama                                    |

| RAG             | Sentence Transformers, Embeddings, Vector Search |

| Tool Protocol   | MCP                                              |

| API             | FastAPI                                          |

| Database        | SQLite                                           |

| Testing         | Pytest                                           |

| Version Control | Git, GitHub                                      |



\## Project Structure



```text

marketing-copilot/

├── app/

│   ├── agents/       # Agent workflow and tool selection

│   ├── api/          # FastAPI application

│   ├── llm/          # LLM services and campaign generation

│   ├── mcp/          # MCP client and server

│   ├── rag/          # Embeddings and retrieval

│   └── tools/        # Product, customer and marketing tools

├── data/

│   └── knowledge/    # Product and marketing knowledge

├── tests/             # Automated tests

├── requirements.txt

└── README.md

```



\## Setup



\### 1. Clone



```bash

git clone https://github.com/JafsinJaleel/marketing-copilot.git

cd marketing-copilot

```



\### 2. Create Environment



```cmd

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt

```



\### 3. Start Qwen3



```cmd

ollama pull qwen3:4b

```



\### 4. Run API



```cmd

uvicorn app.api.main:app --reload

```



API:



```text

http://127.0.0.1:8000

```



Swagger:



```text

http://127.0.0.1:8000/docs

```



\## Example



\*\*Request\*\*



```json

{

&#x20; "message": "Create a marketing campaign for SmartFit Watch targeting working professionals."

}

```



The agent:



1\. Classifies the request

2\. Selects required tools

3\. Retrieves product, customer, and marketing context

4\. Generates the campaign using Qwen3

5\. Validates the campaign

6\. Retries if required sections are missing



\## Testing



Run:



```cmd

pytest -q

```



\## Author



\*\*Jafsin Jaleel\*\*



B.Tech Computer Science \& Engineering



GitHub: \[JafsinJaleel](https://github.com/JafsinJaleel)



```



\*\*This is the version I'd use.\*\* It is concise, technical, and recruiter-friendly without making the README unnecessarily huge.



One small note: after pasting this, GitHub will render the architecture diagram as a clean code diagram, so you don't need to create a separate architecture image yet.

```



