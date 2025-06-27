import logging
from src.exception import CustomException

import os
import pandas as pd
import json
import sys

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class DataIngestion:
    def __init__(self,file_path:str):
        try:
            self.file_path = file_path
            logging.info("file_path is correct")
        except Exception as e:
            raise CustomException(e,sys)
        
    def load_data(self):
        '''
        loading the data  
        '''
        _, extension = os.path.splitext(self.file_path)
        extension = extension.lower()

        if extension == '.json':
            try:
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                logging.info("data loaded successfully")
                return data, extension
            except Exception as e:
                raise CustomException(e, sys)
        elif extension == '.csv':
            try:
                data = pd.read_csv(self.file_path)
                logging.info("data loaded successfully")
                return data, extension
            except Exception as e:
                raise CustomException(e, sys)
        else:
            raise CustomException(f"Unsupported file extension: {extension}", sys)

    def convertToDocs(self):
        try:
            splitter = RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=10)
            logging.info("splitter initialized successfully")
        except Exception as e:
            raise CustomException(e,sys)
        
        data,extension = self.load_data()

        if extension == '.json':
            try:
                doc = [Document(str(data))]
                docs = splitter.split_documents(documents=doc)
                logging.info("documents splitted")
            except Exception as e:
                raise CustomException(e,sys)
            
            return docs

        elif extension == '.csv':
            try:
                if 'prompt' not in data.columns or 'response' not in data.columns:
                    raise ValueError("CSV must contain 'prompt' and 'response' columns")
                
                QA = []
                for idx, (prompt, response) in enumerate(zip(data[data.columns[0]], data[data.columns[1]])):
                    QA.append({
                        'question': prompt, 'answer': response
                    })

                doc = [Document(str(QA))]
                docs = splitter.split_documents(documents=doc)
                logging.info("documents splitted")
                return docs
            except Exception as e:
                raise CustomException(e, sys)
        else:
            raise CustomException(f"Unsupported file extension for document conversion: {extension}", sys)
        