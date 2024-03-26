from typing import Dict, List
from .base_service import BaseService
from repositories.competences_repository import CompetenceRepository

class CompetencesService(BaseService):

    def __init__(self) -> None:
        super().__init__()
        self._setRepository(CompetenceRepository(self._connection))

    
    def get_by_area(self, area_tag: str, withHabilities: bool) -> List[Dict]:
        area = self._repository.get_by_area(area_tag,withHabilities)
        return area
    