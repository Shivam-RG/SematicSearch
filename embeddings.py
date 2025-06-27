from src.sematicsearch_api.search import SematicRetriever,Embeddings

from data_pipeline import DataPipeline

import pickle
from src.logger import logging
from src.exception import CustomException

import sys
import os


pipeline = DataPipeline(r'C:\Users\Meta\Downloads\Sematic\SematicSearch\data\faqs.json')
docs = pipeline.getDocs()

# Embeddings,VectorStore,Retriever and Seamtic Search

class EmbeddingPipeline:
    def embeddingAndVectordb(self):
        embedder = Embeddings()
        embedder.getEmbeddings()
        vectordb = embedder.VectorDB(docs=docs)

        return vectordb
    

embedding = EmbeddingPipeline()
vectordb = embedding.embeddingAndVectordb()
retrieve = SematicRetriever(vectordb=vectordb)
retriever = retrieve.getRetriever()

ARTIFACTS = 'artifacts'
project_root = r'C:\Users\Meta\Downloads\Sematic\SematicSearch'

path = os.path.join(project_root, ARTIFACTS)


try:
    os.makedirs(path, exist_ok=True)
    with open(f"{path}\\retriever.pkl",'wb') as f:
        pickle.dump(retriever,f)
    logging.info("retriever saved to the artifacts folder")
except Exception as e:
    raise CustomException(e,sys)
