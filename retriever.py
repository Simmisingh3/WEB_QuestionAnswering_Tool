import os
import requests
import chromadb
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve OpenRouter API Key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("⚠️ OpenRouter API Key is missing! Please set OPENROUTER_API_KEY in your .env file.")

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("qa_data")

def get_answer(question, data_store):
    """
    Retrieves the most relevant answer from the ingested content using ChromaDB and OpenRouter API.

    Parameters:
        question (str): User's question.
        data_store (dict): Dictionary containing {URL: content} pairs.

    Returns:
        str: Answer extracted from relevant text.
    """
    try:
        # Store extracted content in ChromaDB (Ensuring no duplicates)
        for url, content in data_store.items():
            if not collection.get(ids=[url])["ids"]:  # Check if URL already exists
                collection.add(
                    documents=[content],  # ChromaDB expects a list
                    metadatas=[{"source": url}],  # Metadata for tracking sources
                    ids=[url]  # Unique ID per URL
                )

        # Query ChromaDB for relevant content
        results = collection.query(query_texts=[question], n_results=1)

        if not results or "documents" not in results or not results["documents"]:
            return "No relevant content found."

        relevant_text = results["documents"][0]  # Get most relevant text

        # Use OpenRouter API to generate an answer
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",  # OpenRouter's API URL
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",  # Adjust based on available models in OpenRouter
                "messages": [
                    {"role": "system", "content": "Answer strictly based on the provided text."},
                    {"role": "user", "content": f"Context: {relevant_text}\nQuestion: {question}"}
                ]
            }
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"⚠️ OpenRouter API Error: {response.json()}"

    except Exception as e:
        print(f"Unexpected Error in get_answer: {str(e)}")  # Debugging unexpected errors
        return f"An error occurred: {str(e)}"
