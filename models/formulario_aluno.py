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
    def __init__(self,_id,professor:Professor,grafos:list[Grafo] = []) -> None:
        self.__id = _id
        if(not isinstance(professor,Professor)):
            self.__professor = Professor(**professor)
        else: 
            self.__professor = professor
        
        if grafos != []:
            if not isinstance(grafos[0],Grafo):
                grafos = FormularioUtils.toGrafoList(grafos)
        
        self.__grafos_das_respostas = grafos
        self.__data_criacao = datetime.now()

    def __validate_data(data):
    # Check if the main keys exist in the dictionary
        if not isinstance(data, dict):
            return False
        if 'disciplina' not in data or 'competencias' not in data:
            return False

        # Check if the types of the values are correct
        if not isinstance(data['disciplina'], int):
            return False
        if not isinstance(data['competencias'], dict):
            return False

        return True
    
    def getAluno(self):
        return self.__professor
    
    def getGrafos(self):
        return self.__grafos_das_respostas
    
    def appendNewGrafo(self,disciplinasArea,values):
        self.__grafos_das_respostas = FormularioUtils.montaRepostaParaDisciplina(disciplinasArea,values,self.__grafos_das_respostas)

    def to_dict(self):
        if self.__id == None:
            return {
            "professor": self.__professor.to_dict(),
            "grafos": [grafo.to_dict() for grafo in self.__grafos_das_respostas],
            "data_criacao": self.__data_criacao
            
        }
        return {
            "_id": self.__id,
            "professor": self.__professor.to_dict(),
            "grafos": [grafo.to_dict() for grafo in self.__grafos_das_respostas],
            "data_criacao": self.__data_criacao
        }