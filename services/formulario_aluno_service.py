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
        

    def get_by_aluno(self, aluno: Aluno) -> List[Dict]:
        formulario = self._repository.get_by_aluno(aluno)
        return formulario
    
    def insert_formulario(self,data_form:Dict) -> List[Dict]:
        aluno: Aluno = Aluno(**data_form["aluno"])
        grafo_values: Dict = data_form["respostas"]

        disciplineRepository = DisciplineRepository(self._connection)

        if "disciplina" not in grafo_values:
            print("Disciplina não encontrada")
            
            return self._repository.insert_one(FormularioAluno(aluno,[]).to_dict())

        disciplina = disciplineRepository.get_by_id(grafo_values["disciplina"])

        disciplinasDaArea = disciplineRepository.get_by_area(disciplina["area"])

        formFound:FormularioAluno =  self._repository.get_by_aluno(aluno)

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