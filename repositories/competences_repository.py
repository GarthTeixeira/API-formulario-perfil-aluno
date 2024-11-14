from .base_repository import BaseRepository
from typing import Dict, List
from datetime import datetime

class CompetenceRepository(BaseRepository):
    def __init__(self, connection):
        print("CompetenceRepository")
        super().__init__(connection, "competencias")      
       
    def get_by_area(self, area_tag: str, withHabilities: bool) -> List[Dict]:
        collection = self._connection.get_collection(self._collection_name)
        filter = {} if withHabilities else {"competencias_habilidades": 0}
        data = collection.find({"tag": area_tag}, filter)
        response = list(data)
        
        return response
    