from .professor import Professor 
from .resposta import Resposta
class Grafo:
    def __init__(self,competencia, arestas):
        self._competencia = competencia

        if arestas != []:
            if not isinstance(arestas[0],Resposta):
                arestas = [Resposta(**aresta) for aresta in arestas]

        self._arestas = arestas

    def getRespostas(self,diciplina_id):
        return list(filter(lambda resposta: resposta.origem == diciplina_id, self.arestas))
    

    def getCompetencia(self):
        return self._competencia
    
    def getArestas(self):
        return self._arestas

    def setRespostasValue(self,disciplina_origem,valor,disciplinas_destino):
        # aresta = next((resposta for resposta in self._arestas if resposta['origem'] == disciplina_origem), None)
        for resposta in  self._arestas:
            print(type(resposta))
            if resposta.origem == disciplina_origem:
                resposta.valor = valor
                return
        else:
            self._arestas.append(Resposta(disciplina_origem,valor,disciplinas_destino))

      

    def montaArestaGrafo(disciplinaOrigem,valor,disciplinasDestino):
        disciplinasDestinoStr = list(map(lambda disciplina: str(disciplina['_id']), disciplinasDestino))
        return [
            Resposta(disciplinaOrigem,valor,disciplinasDestinoStr)
        ]
        

    def __str__(self):
        return f"Competencia: {self._competencia}\nArestas: {len(self._arestas)}"
    
    def print(self):
        print(self.__str__())
        print(":[")
        for aresta in self._arestas:
            print("  {")
            aresta.print()
            print("  } \n")
        print("]")

    def to_dict(self):
        return {
            "competencia": self._competencia,
            "arestas": [aresta.to_dict() for aresta in self._arestas]
        }