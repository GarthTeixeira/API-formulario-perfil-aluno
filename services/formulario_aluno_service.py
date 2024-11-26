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
        school: any = professor_data['escola']
        turma:any = professor_data['turma']['_id']
        professor: Professor = Professor(professor_data["nome"],professor_data["email"])
       
        form_response = self._repository.get_by_school_and_turma(school,turma)
        response = {}
        if (len(form_response) != 0):
            form = FormularioAluno(**form_response[0])
            form.appendNewProfessor(professor)
            response = self._repository.update_formulario(form.to_dict())
        else:
            response = self._repository.insert_one(FormularioAluno(None,[professor],school,turma).to_dict())
        print("Novo Professor Inserido")
        professor.exibir_informacoes()
        self.closeConnection()
        return response
    
    def insert_resposta(self, grafo_values: Dict ) -> List[Dict]:
        area = grafo_values['area']
        formulario_id = grafo_values["professor"]
        reponse = {}
        formFound = self._repository.get_by_id(formulario_id)

        formulario = FormularioAluno(**formFound)

        escola_id = formulario.getEscola()

        disciplina_id = grafo_values['disciplina']
        
        disciplina = EscolaService().get_disciplina_by_id(escola_id,disciplina_id)        

        serie_ano_seguinte = disciplina['serie_ano'] + 1;

        if serie_ano_seguinte == 4:
            lastNode = EscolaService().get_last_node(escola_id)
            formulario.appendNewGrafo(lastNode,disciplina,grafo_values['competencias'])
        else:
            if area != 'COGNITIVOS':
                if "disciplina" not in grafo_values:
                    print("Disciplina não encontrada")
                    return []
                
                if(area != disciplina['area']):
                    raise ValueError("Area not compatible with subject")

                disciplinasDaArea = EscolaService().get_school_subjects_by_area_and_serie_ano(escola_id,disciplina["area"], serie_ano_seguinte)
                
                formulario.appendNewGrafo(
                    disciplinasDaArea,
                    disciplina,
                    grafo_values['competencias']
                )
            
            else:
                disciplinas = EscolaService().get_school_subjects_by_serie_ano(escola_id, serie_ano_seguinte)
                formulario.appendNewGrafo(
                    disciplinas,
                    disciplina,
                    grafo_values['competencias']
                )

        
        formularioDict = formulario.to_dict()
        # print("formularioDict",formularioDict)
        reponse = self._repository.update_one(formularioDict["_id"],formularioDict)
        self.closeConnection()
        return reponse
        