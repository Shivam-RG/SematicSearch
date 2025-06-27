from fastapi import FastAPI,HTTPException
from fastapi.responses import HTMLResponse
import os
from src.sematicsearch_api.models import Query,QueryResponse
import pickle

from src.sematicsearch_api.search import Search

from pathlib import Path


# BASE_DIR = Path(__file__).resolve().parent
# artifact_path = BASE_DIR / "artifacts" / "retriever.pkl"

GITHUB_RETRIEVER_URL = "https://github.com/Shivam-RG/SematicSearch/releases/download/v.0.1/retriever.pkl"
LOCAL_PATH = "artifacts/retriever.pkl"

def download_if_not_exists():
    if not os.path.exists(LOCAL_PATH):
        os.makedirs(os.path.dirname(LOCAL_PATH), exist_ok=True)
        print("Downloading retriever.pkl from GitHub release...")
        response = requests.get(GITHUB_RETRIEVER_URL)
        if response.status_code == 200:
            with open(LOCAL_PATH, "wb") as f:
                f.write(response.content)
            print("Download complete.")
        else:
            raise RuntimeError(f"Failed to download retriever.pkl: {response.status_code}")

# Call before loading
download_if_not_exists()

# Then load like usual
with open(LOCAL_PATH, "rb") as f:
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
