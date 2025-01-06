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
    def __init__(self,_id,professores:list[Professor],escola,turma,data_criacao = None,data_atualizacao = None,grafos:list[Grafo] = []) -> None:
        self.__id = _id
        self.__escola = escola
        self.__turma = turma
        if(professores != []):
            if not isinstance(professores[0],Professor):
                professores = FormularioUtils.toProfessoresList(professores)
            
        if grafos != []:
            if not isinstance(grafos[0],Grafo):
                grafos = FormularioUtils.toGrafoList(grafos)
        
        self.__professores = professores
        self.__grafos_das_respostas = grafos

        if(data_criacao == None):
            self.__data_criacao = datetime.now()
            self.__data_atualizacao = self.__data_criacao
        else:
            self.__data_criacao = data_criacao
            self.__data_atualizacao = data_atualizacao
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

    def appendNewProfessor(self,professor):
        self.__professores.append(professor)
        self.__data_atualizacao = datetime.now()

    def appendNewRegisterToProfessor(self,disciplina,tipo,nome,email):
        try:
            professor = next( prof for prof in self.__professores if (prof.email==email and prof.nome == nome))
            resumed_disciplina = {"id":disciplina['_id'], "nome": '{} - {}° ano'.format(disciplina['name'],disciplina['serie_ano'])}
            professor.disciplinas.append({"disciplina": resumed_disciplina, "data_resposta":self.__data_atualizacao,"tipo":tipo})
        except StopIteration:
            raise Exception("professor não encontrado")
    

    def to_dict(self):
        if self.__id == None:
            return {
            "escola": self.__escola,
            "turma":self.__turma,
            "professores": [professor.to_dict() for professor in self.__professores],
            "grafos": [grafo.to_dict() for grafo in self.__grafos_das_respostas],
            "data_criacao": self.__data_criacao,
            "data_atualizacao":self.__data_atualizacao
            
        }
        return {
            "_id": self.__id,
            "escola": self.__escola,
            "turma":self.__turma,
            "professores": [professor.to_dict() for professor in self.__professores],
            "grafos": [grafo.to_dict() for grafo in self.__grafos_das_respostas],
            "data_criacao": self.__data_criacao,
            "data_atualizacao":self.__data_atualizacao
        }