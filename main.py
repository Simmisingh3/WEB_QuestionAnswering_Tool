"""Web Research Q&A API."""
from contextlib import asynccontextmanager
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, HttpUrl

from config import BASE_DIR, MAX_URLS_PER_INGEST, MAX_PAGE_CHARS
from retriever import get_answer, ingest_document
from scraper import scrape_text


class URLInput(BaseModel):
    urls: list[HttpUrl] = Field(min_length=1, max_length=MAX_URLS_PER_INGEST)


class QuestionInput(BaseModel):
    question: str = Field(min_length=2, max_length=2000)
    urls: list[HttpUrl] | None = Field(default=None, max_length=MAX_URLS_PER_INGEST)


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(
    title="Web Research Q&A",
    description="Ask source-grounded questions across public webpages, with citations.",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "web-research-qa", "version": app.version}


@app.post("/api/ingest")
@app.post("/ingest", include_in_schema=False)
def ingest_urls(input_data: URLInput):
    results = []
    for item in input_data.urls:
        url = str(item)
        try:
            text = scrape_text(url, max_chars=MAX_PAGE_CHARS)
            chunk_count = ingest_document(url, text)
            results.append({"url": url, "status": "success", "characters": len(text), "chunks": chunk_count})
        except (ValueError, OSError) as exc:
            results.append({"url": url, "status": "error", "message": str(exc)})
        except Exception:
            results.append({"url": url, "status": "error", "message": "Ingestion failed. Check server logs and configuration."})
    succeeded = sum(item["status"] == "success" for item in results)
    if not succeeded:
        raise HTTPException(status_code=422, detail={"message": "No webpages could be ingested.", "results": results})
    return {"message": f"Ingested {succeeded} of {len(results)} webpage(s).", "results": results}


@app.post("/api/ask")
@app.post("/ask", include_in_schema=False)
def ask_question(input_data: QuestionInput):
    try:
        urls = [str(url) for url in input_data.urls] if input_data.urls else None
        return get_answer(input_data.question.strip(), sources=urls)
    except RuntimeError as exc:
        message = str(exc)
        status = 503 if "not configured" in message.lower() else 502
        raise HTTPException(status_code=status, detail=message) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Question answering failed. Check server logs.") from exc


if (BASE_DIR / "static").is_dir():
    app.mount("/", StaticFiles(directory=BASE_DIR / "static", html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
