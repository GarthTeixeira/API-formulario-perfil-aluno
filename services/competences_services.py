import json as json
from typing import Dict, List
from db_resources.connection import DBConnectionHandler
from repositories.competences_repository import CompetenceRepository

class CompetencesService:

    def __init__(self) -> None:
        db_handler = DBConnectionHandler()
        db_handler.connect_to_db()
        connection = db_handler.get_db_connection()
        self.__competence_repository = CompetenceRepository(connection)

    
    def get_area(self, area_tag: str, withHabilities: bool) -> List[Dict]:
        
        area = self.__competence_repository.get_by_area(area_tag,withHabilities)
      
        return area
    
    def getAll(self) -> List[Dict]:
        competences = self.__competence_repository.get_all()
        return competences