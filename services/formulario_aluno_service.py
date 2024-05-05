from typing import Dict, List
from .base_service import BaseService
from repositories.formulario_aluno_repository import FormularioAlunoRepository
from repositories.disciplines_repository import DisciplineRepository

from models.aluno import Aluno
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
    

    def insert_aluno(self, aluno_data: any) -> List[Dict]:
        aluno: Aluno = Aluno(**aluno_data)
        formulario = self._repository.insert_one(FormularioAluno(None,aluno,[]).to_dict())
        return formulario
    
    def insert_grafo(self, grafo_values: Dict ) -> List[Dict]:
        formulario_id = grafo_values["formulario"]
        if "disciplina" not in grafo_values:
            print("Disciplina não encontrada")
            return []
        
        disciplineRepository = DisciplineRepository(self._connection)
        
        disciplina = disciplineRepository.get_by_id(grafo_values["disciplina"])

        disciplinasDaArea = disciplineRepository.get_by_area(disciplina["area"])

        formFound = self._repository.get_by_id(formulario_id)

        formulario = FormularioAluno(**formFound)

        formulario.appendNewGrafo(
            disciplinasDaArea,
            grafo_values,
           )
        formularioDict = formulario.to_dict()
        resposta = self._repository.update_one(formularioDict["_id"],formularioDict)            

        return resposta
        
    
    def insert_formulario(self,data_form:Dict) -> List[Dict]:
        aluno = data_form["alunoId"]
        grafo_values: Dict = data_form["respostas"]

        disciplineRepository = DisciplineRepository(self._connection)

        disciplina = disciplineRepository.get_by_id(grafo_values["disciplina"])

        disciplinasDaArea = disciplineRepository.get_by_area(disciplina["area"])

        formFound:FormularioAluno =  self.get_by_aluno(aluno)

        formulario = None

        if formFound['id'] is None:
            grafos = FormularioUtils.montaRepostaParaDisciplina(
                disciplinasDaArea,
                grafo_values,
                []
            )
            formFound = FormularioAluno(aluno,grafos)
            formulario = self._repository.insert_formulario(formFound)
        else:  
            formFound.appendNewGrafo(FormularioUtils.montaRepostaParaDisciplina(
                disciplinasDaArea,
                grafo_values))
            formulario = self._repository.update_formulario(formFound)            

        return formulario