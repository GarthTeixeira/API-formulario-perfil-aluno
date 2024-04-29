from .aluno import Aluno 

class Grafo:
    def __init__(self,competencia,arestas):
        self._competencia = competencia
        self._arestas = arestas

    def getRespostas(self,diciplina_id):
        return list(filter(lambda resposta: resposta.origem == diciplina_id, self.arestas))
    

    def getCompetencia(self):
        return self._competencia
    
    def getArestas(self):
        return self._arestas

    def setRespostasValue(self,diciplina_id,valor):
        for index, resposta in enumerate(self._arestas):
            if resposta.origem == str(diciplina_id):
                self._arestas[index].valor = valor

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