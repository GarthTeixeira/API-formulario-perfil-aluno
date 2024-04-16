from models.resposta import Resposta


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
    def montaResposta(disciplinasDaArea, valoresDisciplina, competencia):
        
        disciplinasDaAreaOrdenadasPorSeries = sorted(disciplinasDaArea, key=lambda disciplina: disciplina['serie_ano'])
        anosSet = set(map(lambda disciplina: disciplina['serie_ano'], disciplinasDaAreaOrdenadasPorSeries))

        resposta = {}
        resposta['arestas_grafo'] = []

        for ano in anosSet:
            disciplinasDoAno = list(filter(lambda disciplina: disciplina['serie_ano'] == ano, disciplinasDaAreaOrdenadasPorSeries))
            disciplinasDoAnoSeguinte = list(filter(lambda disciplina: disciplina['serie_ano'] == ano + 1, disciplinasDaAreaOrdenadasPorSeries))

            if len(disciplinasDoAnoSeguinte) != 0:
                print(f"Disciplinas do {ano}º ano (vertice origem):")
                
                for disciplina in disciplinasDoAno:
                    resposta['arestas_grafo'].append(
                        Resposta(
                            disciplina['id'],
                            valoresDisciplina[disciplina['id']],
                            list(map( lambda disciplina: disciplina['id'], disciplinasDoAnoSeguinte))
                        )
                    )

        resposta['competencia'] = competencia

        return resposta
    
  
    
disciplinas = [ {
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

valorResosta = {
    "11": 1,
    "12": 2,
    "13": 3,
    "14": 4,
    "15": 5
}


resposta = FormularioUtils.montaResposta(disciplinas, valorResosta, "Habilidade 1")

print(resposta)