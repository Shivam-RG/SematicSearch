from pydantic import BaseModel
from typing import List
from langchain_core.documents import Document

# User query
class Query(BaseModel):
    text : str

# Response for semantic-search
class QueryResponse(BaseModel):
    results : List[Document]