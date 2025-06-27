from src.sematicsearch_api.dataIngestion import DataIngestion

# DataIngestion

class DataPipeline:
    def __init__(self,file_path:str):
        self.ingestion = DataIngestion(file_path=file_path)
        

    def getDocs(self):
        data,extension = self.ingestion.load_data()
        docs = self.ingestion.convertToDocs()
    
        return docs
