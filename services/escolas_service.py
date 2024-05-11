from .base_service import BaseService
from typing import Dict, List

from repositories.escola_repository import EscolaRepository

class EscolaService(BaseService):
        
    def __init__(self) -> None:
        super().__init__()
        self._setRepository(EscolaRepository(self._connection))

    def get_school_subjects_by_area(self, school: str, area: str) -> List[Dict]:
        schoolArray = self._repository.get_school_by_id_and_subjects_by_area(school, area)
        schoolFound = schoolArray[0]
        disciplinas = schoolFound["disciplinas"]
        return disciplinas
    
    def get_shchools_names(self) -> List[Dict]:
        schools = self._repository.get_shchools_names()
        return schools