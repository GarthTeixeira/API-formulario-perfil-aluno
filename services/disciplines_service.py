from .base_service import BaseService
from typing import Dict, List
from repositories.disciplines_repository import DisciplineRepository

class DisciplinesService(BaseService):
    
        def __init__(self) -> None:
            super().__init__()
            self._setRepository(DisciplineRepository(self._connection))
    
        def get_by_area(self, area_tag: str) -> List[Dict]:
            print(area_tag)
            area = self._repository.get_by_area(area_tag)
            return area
        
        def get_by_ano(self, ano: str) -> List[Dict]:
            disciplines = self._repository.get_by_ano(ano)
            return disciplines
        