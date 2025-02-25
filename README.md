# Web Q&A Tool 
This Project aims to answer all the questions related to a webpage or its link. 

Below is the structure of my prject.
📌 Project Structure
web-qa-tool/
│── backend/
│   │── venv/             # Virtual environment
│   │── main.py           # FastAPI app (API endpoints)
│   │── scraper.py        # Extracts text from URLs
│   │── retriever.py      # Embeds text & retrieves answers
│   │── config.py         # Stores API keys & settings
│   │── requirements.txt  # Dependencies
│── README.md             # Setup guide

# Steps to run this file
1) Copy and extract this file from github
2) After opening the file, change your directory - cd backend
3) Install requirements - pip install -r requirements.txt
4) On terminal - uvicorn main:app --reload
5) Address - http://127.0.0.1:8000/docs
6) a) On the urls Post section, type the URL
exmaple - 
{
  "urls": [
    "https://example.com"
  ]
}
b) On the ask question Post section , type the questions

{
  "question": "What is the main topic of the website?"
}

Example URLs to Ingest:
OpenAI Blog - https://openai.com/research
FastAPI Documentation - https://fastapi.tiangolo.com/
ChromaDB Documentation - https://docs.trychroma.com/
Hugging Face Blog - https://huggingface.co/blog
Machine Learning on Medium - https://towardsdatascience.com/
Example Questions to Ask (After Ingesting Content):
For OpenAI Blog:
What are some recent research breakthroughs from OpenAI?
How does OpenAI describe the future of AI safety?
What models has OpenAI released recently?
For FastAPI Documentation:
How does FastAPI handle authentication?
What is the difference between Depends and Security in FastAPI?
How can I create an async API with FastAPI?
For ChromaDB Documentation:
How can I use ChromaDB to store embeddings?
What is the query method in ChromaDB?
How do I persist a ChromaDB collection?
For Hugging Face Blog:
What are the latest updates in Hugging Face transformers?
How does Hugging Face optimize LLM inference?
What is the purpose of AutoModelForCausalLM?
For Machine Learning on Medium:
What are the key challenges in deploying ML models?
How do decision trees work in machine learning?
What are some real-world applications of reinforcement learning?