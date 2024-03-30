import json as json
from typing import Dict, List
from db_resources.connection import DBConnectionHandler

class BaseService:

    def __init__(self) -> None:
        db_handler = DBConnectionHandler()
        db_handler.connect_to_db()
        self._connection = db_handler.get_db_connection()
        self._repository = None

    def _setRepository(self, repository):
        self._repository = repository

    
    def get_all(self) -> List[Dict]:
        if(self._repository == None):
            raise Exception("Repository not set")
        list = self._repository.get_all()
        return list
    
    def get_by_id(self, id: str) -> Dict:
        if(self._repository == None):
            raise Exception("Repository not set")
        document = self._repository.get_by_id(id)
        return document
    
    def insert_one(self, data: Dict) -> str:
        if(self._repository == None):
            raise Exception("Repository not set")
        document = self._repository.insert_one(data)
        return document
    
    def insert_list_of_documents(self, data: List[Dict]) -> List[Dict]:
        if(self._repository == None):
            raise Exception("Repository not set")
        list = self._repository.insert_list_of_documents(data)
        return list