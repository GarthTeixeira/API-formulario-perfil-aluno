from bson.objectid import ObjectId
from typing import Dict, List

class BaseRepository:
    
    def __init__(self, connection, collection_name: str):
        self._connection = connection
        self._collection_name = collection_name
        

    def get_all(self) -> List[Dict]:
        collection = self._connection.get_collection(self._collection_name)
        data = collection.find()
        response = list(data)
        
        return response
    
    def get_by_id(self, id: str) -> Dict:
        collection = self._connection.get_collection(self._collection_name)
        data = collection.find_one({"_id": ObjectId(id)})
        return data
    
    def insert_one(self, data: Dict) -> str:
        collection = self._connection.get_collection(self._collection_name)
        response = collection.insert_one(data)
        return str(response.inserted_id)
    
    def insert_list_of_documents(self, data: List[Dict]) -> List[Dict]:
        collection = self._connection.get_collection(self._collection_name)
        response = collection.insert_many(data)
        return str(response.inserted_ids)
    
    def update_one(self, id: str, data: Dict) -> Dict:
        collection = self._connection.get_collection(self._collection_name)
        response = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return response