from fastapi import FastAPI,HTTPException
from fastapi.responses import HTMLResponse
import os
from src.sematicsearch_api.models import Query,QueryResponse
import pickle

from src.sematicsearch_api.search import Search

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
artifact_path = BASE_DIR / "artifacts" / "retriever.pkl"


with open(artifact_path,'rb') as f:
    retriever = pickle.load(f)


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def home():
    if os.path.exists("static/index.html"):
        return open("static/index.html").read()
    return "<h1>Sematic Search Microservice</h1>"

@app.post("/sematic")
async def search(input: Query):
    text = input.text.strip()

    if not text:
        raise HTTPException(status_code=400, detail="Text input is required.")
    
    sematic_search = Search(query=text,retriever=retriever)

    result = sematic_search.sematic_results()
    response = QueryResponse(results=result)

    res = []
    for i,doc in enumerate(response.results):
        res.append(str(i) + ". " + doc.page_content)
    
    res = '\n\n'.join(res)
    
    return res
