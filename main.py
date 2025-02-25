from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scraper import scrape_text
from retriever import get_answer

app = FastAPI()
data_store = {}  # Temporary storage for scraped content

class URLInput(BaseModel):
    urls: list[str]

class QuestionInput(BaseModel):
    question: str

@app.post("/ingest")
async def ingest_urls(input_data: URLInput):
    global data_store
    try:
        text_data = {url: scrape_text(url) for url in input_data.urls}
        data_store.update(text_data)
        print("✅ Ingested Data:", data_store)  # Debugging
        return {"message": "Content ingested successfully"}
    except Exception as e:
        print("❌ Ingestion Error:", str(e))  # Debugging
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask") 
async def ask_question(input_data: QuestionInput):
    print("📌 Current Data Store:", data_store)  # Debugging

    if not data_store:
        raise HTTPException(status_code=400, detail="No data available. Ingest content first.")

    try:
        answer = get_answer(input_data.question, data_store)
        print("✅ Generated Answer:", answer)  # Debugging
        return {"answer": answer}
    except Exception as e:
        print("❌ Error in get_answer:", str(e))  # Debugging
        raise HTTPException(status_code=500, detail="Internal Server Error: " + str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
