from models.grafo import Grafo
from models.professor import Professor

class FormularioUtils:
    def __init__(self):
        self.__formularios = []

    def get_formularios(self):
        return self.__formularios

    def add_formulario(self, formulario):
        self.__formularios.append(formulario)

    @staticmethod
    def toGrafoList(grafos):
        return [ Grafo(**grafo) for grafo in grafos]
    
    @staticmethod
    def toProfessoresList(professores):
        return [ Professor(**professor) for professor in professores]


    @staticmethod
    def montaRepostaParaDisciplina(discipinasExistentes ,disciplinaOrigem, competencias, grafosJaExistentes: list[Grafo]) -> list[Grafo]: 
           
        for key,value in competencias.items():
            keysCompetencias = set(map(lambda grafo: grafo.getCompetencia(), grafosJaExistentes)) #Atualiza conjunto de de chaves de competências a cada iteração
            if key in keysCompetencias:
                for grafo in grafosJaExistentes:
                    if grafo.getCompetencia() == key:
                        grafo.setRespostasValue(disciplinaOrigem,value,discipinasExistentes)
                        grafo.print()
                        print("Atualizado !")
              
            else:
                newGrafo = Grafo(key,[])
                newGrafo.setRespostasValue(disciplinaOrigem,value,discipinasExistentes)
                grafosJaExistentes.append(newGrafo)
                newGrafo.print()
                print("Adicionado !")
        
        return grafosJaExistentes

                    
  
    
# disciplinasAreaLinguagens = [ {
#         "name": "Artes",
#         "serie_ano":1,
#         "area": "LINGUAGENS",
#         "escola": "teste",
#         "id": "11"
#     },
#     {
#         "name": "Educacao Fisica",
#         "serie_ano":1,
#         "area": "LINGUAGENS",
#         "escola": "teste",
#         "id": "12"
#     },
#     {
#         "name": "Português",
#         "serie_ano":2,
#         "area": "LINGUAGENS",
#         "escola": "teste",
#         "id": "13"
#     },
#     {
#         "name": "Português",
#         "serie_ano":3,
#         "area": "LINGUAGENS",
#         "escola": "teste",
#         "id": "14"
#     },
#     {
#         "name": "Redação",
#         "serie_ano":3,
#         "area": "LINGUAGENS",
#         "escola": "teste",
#         "id": "15"
#     }]

# disciplinasAreaMatematica = [ {
#         "name": "Matemática I",
#         "serie_ano":1,
#         "area": "MATEMATICA",
#         "escola": "teste",
#         "id": "21"
#     },
#     {
#         "name": "Matemática II",
#         "serie_ano":2,
#         "area": "MATEMATICA",
#         "escola": "teste",
#         "id": "22"
#     },
#     {
#         "name": "Algebra",
#         "serie_ano":3,
#         "area": "MATEMATICA",
#         "escola": "teste",
#         "id": "23"
#     },
#     {
#         "name": "Geometria",
#         "serie_ano":3,
#         "area": "MATEMATICA",
#         "escola": "teste",
#         "id": "24"
#     },
# ]

# valorResposta1 = {
#     "disciplina": 13,
#     "competencias":{
#         "C8":10,
#         "C6":5,
#         "C1":9,
#     }
#     "formulario": 321
# }

# valorResposta2 = {
#     "disciplina": 15,
#     "competencias":{
#         "C8":10,
#         "C6":5,
#         "C1":7,
#     }
# }

# grafos = []
# grafos = FormularioUtils.montaRepostaParaDisciplina(disciplinasAreaLinguagens,valorResposta1,grafos)
# grafos = FormularioUtils.montaRepostaParaDisciplina(disciplinasAreaLinguagens,valorResposta2,grafos)

# for grafo in grafos:
#     grafo.print()