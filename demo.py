from src.logger import logging
from src.exception import CustomException
import sys

from src.sematicsearch_api.dataIngestion import DataIngestion

from src.sematicsearch_api.search import Embeddings,SematicRetriever,Search

# from SematicSearch.embeddings_pipeline import EmbeddingPipeline


# try:
#     a = 1/2
#     logging.info("division done successfully")
# except Exception as e:
#     logging.error("error occured")
#     raise CustomException(e,sys)


# try:
#     a = 1/0
#     logging.info("division done successfully")
# except Exception as e:
#     raise CustomException(e,sys)


# DataIngestion

ingestion = DataIngestion(file_path=r'C:\Users\Meta\Downloads\Sematic\SematicSearch\data\codebasics_faqs.csv')
data,extension = ingestion.load_data()
docs = ingestion.convertToDocs()


# Embeddings,VectorStore,Retriever and Seamtic Search

embedder = Embeddings()
embedder.getEmbeddings()
vectordb = embedder.VectorDB(docs=docs)

retrieve = SematicRetriever(vectordb=vectordb)
retriever = retrieve.getRetriever()

sematic_search = Search(query='What is the refund policy?',retriever=retriever)

result = sematic_search.sematic_results()

print(result)