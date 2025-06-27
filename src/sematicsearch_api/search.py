import logging
from src.exception import CustomException
import sys 

from typing import List


from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema.vectorstore import VectorStore,VectorStoreRetriever
from langchain_core.documents import Document


class Embeddings:
    def __init__(self,model_name = 'all-distilroberta-v1',
                 device = 'cpu',normalize:bool=True):
        self.model_name = model_name
        self.device = device
        self.normalize = normalize
    
    def getEmbeddings(self):
        try:
            self.embeddings = HuggingFaceEmbeddings(model_name = self.model_name,
                                                    model_kwargs = {'device': self.device},
                                                    encode_kwargs = {'normalize_embeddings': self.normalize})
            logging.info(f"{self.model_name} initialized successfully")
        except Exception as e:
            raise CustomException(e,sys)
    
    def VectorDB(self,docs:List[Document]):
        try:
            vectordb = FAISS.from_documents(docs,embedding=self.embeddings)
            logging.info("embeddings stored in the vector database")

            return vectordb
        except Exception as e:
            raise CustomException(e,sys)

class SematicRetriever:
    def __init__(self,vectordb:VectorStore):
        self.vectordb = vectordb
    
    def getRetriever(self):
        try:
            retriever = self.vectordb.as_retriever(search_kwargs={'k':3})
            logging.info("retriever created")
        except Exception as e:
            raise CustomException(e,sys)

        return retriever

class Search:
    def __init__(self,query:str,retriever:VectorStoreRetriever):
        self.query = query
        self.retriever = retriever
    
    def sematic_results(self):
        try:
            results = self.retriever.invoke(self.query)
            logging.info("retriever invoked successfully")
        except Exception as e:
            raise CustomException(e,sys)
    
        return results

