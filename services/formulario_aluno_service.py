from typing import Dict, List
from .base_service import BaseService
from repositories.formulario_aluno_repository import FormularioAlunoRepository
from repositories.disciplines_repository import DisciplineRepository
from repositories.escola_repository import EscolaRepository
from .escolas_service import EscolaService

from models.professor import Professor
from models.grafo import Grafo
from models.formulario_aluno import FormularioAluno

from utils.formularioUtils import FormularioUtils

class FormularioAlunoService(BaseService):
    
    def __init__(self) -> None:
        super().__init__()
        self._setRepository(FormularioAlunoRepository(self._connection))
        

    def get_by_aluno(self, alunoId: str) -> List[Dict]:
        formulario = self._repository.get_by_id(alunoId)
        return formulario
    
    def get_by_school(self, schoolId:str)->List[Dict]:
        return self._repository.get_by_school_id(schoolId)
        

    def insert_professor(self, professor_data: any) -> List[Dict]:
        professor: Professor = Professor(**professor_data)
        formulario = self._repository.insert_one(FormularioAluno(None,professor,[]).to_dict())
        return formulario
    
    def insert_resposta(self, grafo_values: Dict ) -> List[Dict]:
        area = grafo_values['area']
        formulario_id = grafo_values["professor"]
        reponse = {}
        formFound = self._repository.get_by_id(formulario_id)

        formulario = FormularioAluno(**formFound)

        escola_id = formulario.getAluno().to_dict()['escola']

        disciplina_id = grafo_values['disciplina']
        
        disciplina = EscolaService().get_disciplina_by_id(escola_id,disciplina_id)        
        
        if area != 'COGNITIVOS':
            # ???? o q isso faz?
            if "disciplina" not in grafo_values:
                print("Disciplina não encontrada")
                return []
             
            if(area != disciplina['area']):
                raise ValueError("Area not compatible with subject")

            serie_ano = disciplina['serie_ano']

            disciplinasDaArea = EscolaService().get_school_subjects_by_area_and_serie_ano(escola_id,disciplina["area"], serie_ano + 1)
            
            formulario.appendNewGrafo(
                disciplinasDaArea,
                grafo_values,
            )
          
        else:
            disciplinas = EscolaService().get_school_subjects_by_serie_ano(escola_id,disciplina['serie_ano'])
            formulario.appendNewGrafo(
                disciplinas,
                grafo_values,
            )

        
        formularioDict = formulario.to_dict()
        # print("formularioDict",formularioDict)
        reponse = self._repository.update_one(formularioDict["_id"],formularioDict)

        return reponse
        