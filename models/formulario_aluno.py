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
    def __init__(self,_id,professor,school,data_criacao,grafos:list[Grafo] = []) -> None:
        self.__id = _id
        self.__escola = school
        self.__professores = []
        if(not isinstance(professor,Professor)):
            self.__professores.add(Professor(**professor))
        else: 
            self.__professores.add(professor)
        
        if grafos != []:
            if not isinstance(grafos[0],Grafo):
                grafos = FormularioUtils.toGrafoList(grafos)
        
        self.__grafos_das_respostas = grafos
        self.__data_criacao = datetime.now()
    
    def getAluno(self):
        return self.__professor
    
    def getGrafos(self):
        return self.__grafos_das_respostas
    
    def getId(self):
        return self.__id
    
    def appendNewGrafo(self,disciplinasExistentes,disciplinaOrigem, competencias):
        self.__grafos_das_respostas = FormularioUtils.montaRepostaParaDisciplina(disciplinasExistentes,disciplinaOrigem, competencias,self.__grafos_das_respostas)

    def to_dict(self):
        if self.__id == None:
            return {
            "escola": self.__escola,
            "professores": [professor.to_dict() for professor in self.__professores],
            "grafos": [grafo.to_dict() for grafo in self.__grafos_das_respostas],
            "data_criacao": self.__data_criacao
            
        }
        return {
            "_id": self.__id,
            "escola": self.__escola,
            "professores": [professor.to_dict() for professor in self.__professores],
            "grafos": [grafo.to_dict() for grafo in self.__grafos_das_respostas],
            "data_criacao": self.__data_criacao
        }