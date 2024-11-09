from models.professor import Professor
from models.grafo import Grafo
from utils.formularioUtils import FormularioUtils
from datetime import datetime

# Resquest format
# {
#     "disciplina": 0,
#     "competencias":dict
# }

class FormularioAluno:
    def __init__(self,_id,professor,school,turma,grafos:list[Grafo] = []) -> None:
        self.__id = _id
        self.__escola = school
        self.__turma = turma
        self.__professores = []
        if(not isinstance(professor,Professor)):
            self.__professores.append(Professor(**professor))
        else: 
            self.__professores.append(professor)
        
        if grafos != []:
            if not isinstance(grafos[0],Grafo):
                grafos = FormularioUtils.toGrafoList(grafos)
        
        self.__grafos_das_respostas = grafos
        self.__data_criacao = datetime.now()
        self.__data_atualizacao = self.__data_criacao
    
    def getAluno(self):
        return self.__professor
    
    def getEscola(self):
        return self.__escola
    
    def getGrafos(self):
        return self.__grafos_das_respostas
    
    def getId(self):
        return self.__id
    
    def appendNewGrafo(self,disciplinasExistentes,disciplinaOrigem, competencias):
        self.__grafos_das_respostas = FormularioUtils.montaRepostaParaDisciplina(disciplinasExistentes,disciplinaOrigem, competencias,self.__grafos_das_respostas)
        self.__data_atualizacao = datetime.now()

    def to_dict(self):
        if self.__id == None:
            return {
            "escola": self.__escola,
            "truma":self.__turma,
            "professores": [professor.to_dict() for professor in self.__professores],
            "grafos": [grafo.to_dict() for grafo in self.__grafos_das_respostas],
            "data_criacao": self.__data_criacao,
            "data_atualizacao":self.__data_atualizacao
            
        }
        return {
            "_id": self.__id,
            "escola": self.__escola,
            "truma":self.__turma,
            "professores": [professor.to_dict() for professor in self.__professores],
            "grafos": [grafo.to_dict() for grafo in self.__grafos_das_respostas],
            "data_criacao": self.__data_criacao,
            "data_atualizacao":self.__data_atualizacao
        }