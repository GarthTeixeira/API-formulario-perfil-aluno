from typing import Dict, List
from .base_service import BaseService
from repositories.formulario_aluno_repository import FormularioAlunoRepository
from repositories.disciplines_repository import DisciplineRepository
from repositories.escola_repository import EscolaRepository
from .escolas_service import EscolaService

from models.professor import Professor
from models.grafo import Grafo
from models.formulario_aluno import FormularioAluno
from models.escola import Escola

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
    
    def get_teatcher_and_class_by_school(self, schoolId:str)-> List[Dict]:
        return self._repository.get_teacher_by_school_id(schoolId)
    
    def get_subject_teatchers_registers(self, form_id) -> List[Dict]:
        return self._repository.get_subject_teatchers_registers(form_id)
    
    def insert_professor_for_multiple_turmas(self,professor_data:any) -> List[Dict]:
        list_reponse = []
        #TODO: não otimizado, pois está iterando sobre o dado e realizando operação por operação
        for turma in professor_data['escola']['turmas']:
            professor_data['turma'] = turma
            list_reponse.append(self.__insert_professor(professor_data))
        self.closeConnection()
        return list_reponse

    def __insert_professor(self, professor_data: any) -> Dict:
        school, turma, professor = self.__extractFromProfessorData(professor_data)
        form_id = self.__updateOrCreateFormAluno(school, turma['_id'], professor)
        print("Novo Professor inserido no formulário {} (turma: {} serie: {})".format(form_id, turma['nome'], turma['serie']))
        professor.exibir_informacoes()
        return {'professor':professor.to_dict(), '_id': form_id}
      
    
    def __updateOrCreateFormAluno(self, escola ,turma_id, professor):
        form_response = self._repository.get_by_turma(turma_id)
        if (form_response is not None):
            form = FormularioAluno(**form_response)
            form.appendNewProfessor(professor)
            return self._repository.update_formulario(form.to_dict())
        else:
            return self._repository.insert_one(FormularioAluno(None,[professor],escola,turma_id).to_dict())
    
    def __extractFromProfessorData(self,professor_data:any):
        escola: Escola = Escola(professor_data['escola']['id'],professor_data['escola']['nome'])
        turma:any = professor_data['turma']
        professor: Professor = Professor(professor_data["nome"],professor_data["email"], professor_data["telefone"])
        return (escola, turma, professor)
    
    #TODO: Refatorar cleanly
    def insert_resposta(self, grafo_values: Dict ) -> List[Dict]:
        area = grafo_values['area']
        formulario_id = grafo_values["formulario"]
        reponse = {}
        formFound = self._repository.get_by_id(formulario_id)

        formulario = FormularioAluno(**formFound)
        escola_id = formulario.getEscola().getEscolaId()
        disciplina_id = grafo_values['disciplina']
        
        disciplina = EscolaService().get_disciplina_by_id(escola_id,disciplina_id)

        if(disciplina is None):
            raise Exception(f"Não existem disciplinas correspondentes a escola_id:'{escola_id}', disciplina_id:'{disciplina_id}'")         

        serie_ano_seguinte = disciplina['serie_ano'] + 1
        tipo = "COG" if area == 'COGNITIVOS' else "AREA"

        if serie_ano_seguinte == 4:
            lastNode = EscolaService().get_last_node(escola_id)
            formulario.appendNewGrafo(lastNode,disciplina,grafo_values['competencias'])
        else:
            if tipo != 'COG':
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
                
        formulario.appendNewRegisterToProfessor(
                disciplina,
                tipo,
                **grafo_values["professor"]
            )

                
        formularioDict = formulario.to_dict()
        reponse = self._repository.update_one(formularioDict["_id"],formularioDict)
        self.closeConnection()
        return reponse
        