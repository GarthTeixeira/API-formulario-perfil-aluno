from models.aluno import Aluno
from models.grafo import Grafo
from utils.formularioUtils import FormularioUtils
# Resquest format
# {
#     "disciplina": 0,
#     "competencias":dict
# }

class FormularioAluno:
    def __init__(self,aluno:Aluno,grafos:list[Grafo] = []) -> None:
        self.__aluno = aluno
        self.__grafos_das_respostas = grafos

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
        return self.__aluno
    
    def getGrafos(self):
        return self.__grafos_das_respostas
    
    def appendNewGrafo(self,values,disciplinasArea):
        if(self.__validate_data(values)):
            self.__grafos_das_respostas = FormularioUtils.montaRepostaParaDisciplina(disciplinasArea,values,self.__grafos_das_respostas)

    def to_dict(self):
        return {
            "aluno": self.__aluno.to_dict(),
            "grafos": [grafo.to_dict() for grafo in self.__grafos_das_respostas]
        }