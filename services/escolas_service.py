from .base_service import BaseService
from typing import Dict, List

from repositories.escola_repository import EscolaRepository

test = 0

class EscolaService(BaseService):
        
    def __init__(self) -> None:
        super().__init__()
        self._setRepository(EscolaRepository(self._connection))

    def get_school_subjects_by_area(self, school: str, area: str) -> List[Dict]:
        schoolArray = self._repository.get_school_by_id_and_subjects_by_area(school, area)
        if len(schoolArray) == 0:
            return []
        schoolFound = schoolArray[0]
        disciplinas = schoolFound["disciplinas"]
        return disciplinas

    def get_school_subjects_by_area_and_serie_ano(self, school: str, area: str, serie_ano: int) -> List[Dict]:
        schoolArray = self._repository.get_school_by_id_and_subjects_by_area_and_serie_ano(school, serie_ano, area)
        if len(schoolArray) == 0:
            return []
        schoolFound = schoolArray[0]
        disciplinas = schoolFound["disciplinas"]
        return disciplinas
    
    def get_last_node(self,school:str):
        schoolArray = self._repository.get_school_by_id_last_node(school)
        if(len(schoolArray)) == 0:
            return []
        schoolFound = schoolArray[0]
        last_node_array = schoolFound["disciplinas"]
        if (len(last_node_array)) !=1:
            print("erro, mais de uma formatura encontrada!!!!")

        return last_node_array
        
    
    def get_all_disciplinas_by_school(self, school: str):
        schoolArray = self._repository.get_school_disciplinas(school)
        if len(schoolArray) == 0:
            return []
        schoolFound = schoolArray[0]
        disciplinas = schoolFound["disciplinas"]
        return disciplinas
    
    def get_school_subjects_by_serie_ano(self, school: str, serie_ano:int) -> List[Dict]:
        schoolArray = self._repository.get_school_by_id_and_subjects_by_area_and_serie_ano(school, serie_ano)
        if len(schoolArray) == 0:
            return []
        schoolFound = schoolArray[0]
        disciplinas = schoolFound["disciplinas"]
        return disciplinas
    
    def get_disciplina_by_id(self, school: str, disciplina: str) -> List[Dict]:
        schoolsFound = self._repository.get_school_and_disciplina_by_id(school, disciplina)
        if len(schoolsFound) == 0:
            return []
        schoolsFound = schoolsFound[0]
        disciplina = schoolsFound["disciplinas"][0]
        return disciplina
    
    def get_schools_names(self) -> List[Dict]:
        schools = self._repository.get_shchools_names()
        return schools
    
    def get_school_classes(self, school: str) -> List[Dict]:
        schoolArray = self._repository.get_school_classes(school)
        if len(schoolArray) == 0:
            return []
        schoolFound = schoolArray[0]
        classes = schoolFound["turmas"]
        return classes