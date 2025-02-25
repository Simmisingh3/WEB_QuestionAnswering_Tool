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

│   |── README.md             # Setup guide

# Steps to run this file
1) Copy and extract this file from github

2) After opening the file, On terminal(Command prompt) activate the virtual environment - backend\venv\Scripts\activate

3) Change the directory(On terminal) - cd backend

3) On terminal, Install requirements - pip install -r requirements.txt

4) On terminal - uvicorn main:app --reload

5) Address - http://127.0.0.1:8000/docs

6) a) On the urls Post section, type the URL

exmaple - 

{
  "urls": [
    "https://huggingface.co/docs/transformers/index"
  ]
}
b) On the ask question Post section , type the questions

{
  "question": "What is machine learning?"
}

Output from the above question - 

{
  "answer": "Machine learning is a field of artificial intelligence that involves the development of algorithms and models that allow computers to learn and make predictions or decisions without being explicitly programmed."
}

Example of some famous URLs to Ingest:

Scikit-Learn - https://scikit-learn.org/stable/user_guide.html

TensorFlow - https://www.tensorflow.org/

PyTorch - https://pytorch.org/docs/stable/index.html

Hugging Face Transformers - https://huggingface.co/docs/transformers/index

ChromaDB - https://docs.trychroma.com/

Example questions-

"What are the latest advancements in reinforcement learning?"

"How does PyTorch handle backpropagation?"

"What are some real-world applications of LLMs?"
