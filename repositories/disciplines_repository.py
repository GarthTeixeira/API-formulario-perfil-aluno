from .base_repository import BaseRepository
from typing import Dict, List

class DisciplineRepository(BaseRepository):
    def __init__(self, connection):
        super().__init__(connection, "disciplinas")
        
       
    def get_by_area(self, area_tag: str) -> List[Dict]:
        collection = self._connection.get_collection(self._collection_name)
        data = collection.find({"area": area_tag})
        response = list(data)
        
        return response
    
    def get_by_ano(self, ano: str) -> List[Dict]:
        collection = self._connection.get_collection(self._collection_name)
        data = collection.find({"ano": ano})
        response = list(data)
        
        return response