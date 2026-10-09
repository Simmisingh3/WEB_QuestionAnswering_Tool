# Web Research Q&A

A source-grounded web research assistant built with FastAPI, ChromaDB, and OpenRouter. Ingest public webpages, ask natural-language questions across their content, and receive answers with source excerpts and citations.

## Highlights

- **Retrieval-augmented generation (RAG):** overlapping text chunks, persistent vector search, and multi-source context.
- **Citations:** answers include inline source markers and structured source excerpts.
- **Safer ingestion:** HTTP(S)-only URLs, checks against local/private IP targets, bounded redirects, request timeouts, HTML-only responses, and content-size limits.
- **API-first:** interactive OpenAPI docs at `/docs`, health endpoint, structured request validation, and backward-compatible `/ingest` and `/ask` routes.
- **Configurable:** model, vector store, chunking, request timeout, and retrieval depth are environment settings.
- **Privacy-minded:** API keys are read from environment variables; secrets and generated databases should not be committed.

## Quick start

Python 3.11 or 3.12 is recommended.

```bash
git clone https://github.com/Simmisingh3/WEB_QuestionAnswering_Tool.git
cd WEB_QuestionAnswering_Tool
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

Create your local environment file:

```bash
cp .env.example .env
```

On Windows, copy `.env.example` to `.env` manually if `cp` is unavailable. Add your **newly generated** OpenRouter API key to `.env`:

```dotenv
OPENROUTER_API_KEY=your_new_key_here
OPENROUTER_MODEL=openai/gpt-4o-mini
```

Start the server:

```bash
uvicorn main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). The browser UI is served at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## API

### Ingest webpages

`POST /api/ingest`

```json
{
  "urls": [
    "https://fastapi.tiangolo.com/",
    "https://docs.trychroma.com/"
  ]
}
```

Each URL reports success or a safe error. Text is split into overlapping chunks and indexed with source metadata.

### Ask a question

`POST /api/ask`

```json
{
  "question": "How does FastAPI validate request data?"
}
```

Optional `urls` can restrict retrieval to previously ingested sources:

```json
{
  "question": "Compare these tools' retrieval approaches",
  "urls": ["https://docs.trychroma.com/"]
}
```

Responses contain `answer` and a `sources` array with source URL, chunk number, and excerpt. A citation is evidence to inspect, not a guarantee that the model interpreted it perfectly.

### Health

`GET /api/health`

## Configuration

See `.env.example`. The default vector database is a local `chroma_db/` directory. Keep it out of version control; the index can be rebuilt by ingesting sources again.

## Tests

```bash
pytest -q
```

Tests focus on deterministic text extraction and chunking. Live website ingestion and model responses require network access and a valid provider key.

## Security notes

- Never commit `.env`, API keys, or local vector database files.
- Rotate any key that was previously committed to a public repository. Removing a file from the latest commit does not erase it from Git history.
- URL checks mitigate common SSRF risks, but public-facing deployments should additionally use outbound network restrictions, rate limiting, authentication, and a dedicated worker.
- This demo does not implement user accounts or per-user data isolation; do not deploy it as a multi-tenant service without those controls.

## Architecture

`URL -> safe HTML fetch -> text extraction -> overlapping chunks -> ChromaDB retrieval -> OpenRouter LLM -> answer + source excerpts`

## License

No license is currently declared. Add a license before accepting external contributions or distributing the project.
