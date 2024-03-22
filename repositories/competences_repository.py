from bson.objectid import ObjectId
from typing import Dict, List
from datetime import datetime

class CompetenceRepository:
    def __init__(self, connection):
        self.__connection = connection
        self.__collection_name = 'competencias_enem_collection'
       
    def get_by_area(self, area_tag: str, withHabilities: bool) -> List[Dict]:
        collection = self.__connection.get_collection(self.__collection_name)
        filter = {} if withHabilities else {"competencias_habilidades": 0}
        data = collection.find({"tag": area_tag}, filter)
        response = list(data)
        
        return response
    
    def get_all(self) -> List[Dict]:
        collection = self.__connection.get_collection(self.__collection_name)
        data = collection.find()
        response = list(data)
        
        return response
    
    def get_by_id(self, id: str) -> Dict:
        collection = self.__connection.get_collection(self.__collection_name)
        data = collection.find_one({"_id": ObjectId(id)})
        return data