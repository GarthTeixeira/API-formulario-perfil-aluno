from models.resposta import Resposta
from models.grafo import Grafo

class FormularioUtils:
    def __init__(self):
        self.__formularios = []

    def get_formularios(self):
        return self.__formularios

    def add_formulario(self, formulario):
        self.__formularios.append(formulario)

    
    def agrupar_reposta_por_competencia(self, repostas_do_questionario):
        competencias = set(map(lambda resposta: resposta.competencia, repostas_do_questionario))
        repostas_agrupadas = []

        for competencia in competencias:

            disciplina_valor_da_competencia = list(filter(lambda resposta: resposta.competencia == competencia, repostas_do_questionario))
            mapa = {objeto.disciplina: objeto.valor for objeto in disciplina_valor_da_competencia}
            
            resposta_agrupada = { 'competencia': competencia, 'mapa': mapa } 
            repostas_agrupadas.append(resposta_agrupada)

        return repostas_agrupadas
    

    @staticmethod
    def montaRepostaParaDisciplina(discipinas,valoresResposta, grafos: list[Grafo]) -> list[Grafo]: 
           
        for key,value in valoresResposta['competencias'].items():
            keys = set(map(lambda grafo: grafo.getCompetencia(), grafos))
            if key in keys:
                for grafo in grafos:
                    if grafo.getCompetencia() == key:
                        grafo.setRespostasValue(valoresResposta['disciplina'],value)
              
            else:
                newGrafo = Grafo(key,FormularioUtils.montaArestaGrafo(discipinas))
                newGrafo.setRespostasValue(valoresResposta['disciplina'],value)
                grafos.append(newGrafo)
        
        return grafos

                

    @staticmethod
    def montaArestaGrafo(disciplinasDaArea):
        
        disciplinasDaAreaOrdenadasPorSeries = sorted(disciplinasDaArea, key=lambda disciplina: disciplina['serie_ano'])
        anosSet = set(map(lambda disciplina: disciplina['serie_ano'], disciplinasDaAreaOrdenadasPorSeries))

        arestas_grafo = []

        for ano in anosSet:
            disciplinasDoAno = list(filter(lambda disciplina: disciplina['serie_ano'] == ano, disciplinasDaAreaOrdenadasPorSeries))
            disciplinasDoAnoSeguinte = list(filter(lambda disciplina: disciplina['serie_ano'] == ano + 1, disciplinasDaAreaOrdenadasPorSeries))

            if len(disciplinasDoAnoSeguinte) != 0:
                
                for disciplina in disciplinasDoAno:
                    arestas_grafo.append(
                        Resposta(
                            disciplina['id'],
                            0,
                            list(map( lambda disciplina: disciplina['id'], disciplinasDoAnoSeguinte))
                        )
                    )

        
        return arestas_grafo
    
  
    
disciplinasAreaLinguagens = [ {
        "name": "Artes",
        "serie_ano":1,
        "area": "LINGUAGENS",
        "escola": "teste",
        "id": "11"
    },
    {
        "name": "Educacao Fisica",
        "serie_ano":1,
        "area": "LINGUAGENS",
        "escola": "teste",
        "id": "12"
    },
    {
        "name": "Português",
        "serie_ano":2,
        "area": "LINGUAGENS",
        "escola": "teste",
        "id": "13"
    },
    {
        "name": "Português",
        "serie_ano":3,
        "area": "LINGUAGENS",
        "escola": "teste",
        "id": "14"
    },
    {
        "name": "Redação",
        "serie_ano":3,
        "area": "LINGUAGENS",
        "escola": "teste",
        "id": "15"
    }]

disciplinasAreaMatematica = [ {
        "name": "Matemática I",
        "serie_ano":1,
        "area": "MATEMATICA",
        "escola": "teste",
        "id": "21"
    },
    {
        "name": "Matemática II",
        "serie_ano":2,
        "area": "MATEMATICA",
        "escola": "teste",
        "id": "22"
    },
    {
        "name": "Algebra",
        "serie_ano":3,
        "area": "MATEMATICA",
        "escola": "teste",
        "id": "23"
    },
    {
        "name": "Geometria",
        "serie_ano":3,
        "area": "MATEMATICA",
        "escola": "teste",
        "id": "24"
    },
]

valorResposta1 = {
    "disciplina": 13,
    "competencias":{
        "C8":10,
        "C6":5,
        "C1":9,
    }
}

valorResposta2 = {
    "disciplina": 15,
    "competencias":{
        "C8":10,
        "C6":5,
        "C1":7,
    }
}

grafos = []
grafos = FormularioUtils.montaRepostaParaDisciplina(disciplinasAreaLinguagens,valorResposta1,grafos)
grafos = FormularioUtils.montaRepostaParaDisciplina(disciplinasAreaLinguagens,valorResposta2,grafos)

for grafo in grafos:
    grafo.print()