# Personal AI Agent

A practical, extensible personal AI assistant with a CLI, FastAPI chat API, SQLite long-term memory, document ingestion, and optional web search.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
# Add OPENAI_API_KEY, or configure another OpenAI-compatible endpoint.
python -m personal_agent.cli chat
```

Run the API:

```bash
uvicorn personal_agent.api:app --reload
```

Then open `http://127.0.0.1:8000/docs`.

## Commands

```bash
python -m personal_agent.cli chat
python -m personal_agent.cli remember "My preferred programming language is Python"
python -m personal_agent.cli search-memory "programming language"
python -m personal_agent.cli ingest path/to/document.txt
```

## Configuration

Copy `.env.example` to `.env`. The default provider is OpenAI-compatible. Ollama can be used locally by setting `LLM_BASE_URL=http://localhost:11434/v1`, `LLM_MODEL=llama3.2`, and leaving the API key blank.

Web search is optional and uses DuckDuckGo's public HTML endpoint. Use it only for non-sensitive queries.

## Safety

The agent does not send email, modify calendars, execute shell commands, or make external changes by default. Those integrations should be added behind explicit confirmation and authentication.
