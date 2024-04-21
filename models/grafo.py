from .aluno import Aluno 

class Grafo:
    def __init__(self,competencia,edges = []):
        self._competencia = competencia
        self.arestas = edges

    def getRespostas(self,diciplina_id):
        return list(filter(lambda resposta: resposta.origem == diciplina_id, self.arestas))
    

    def getCompetencia(self):
        return self._competencia

    def setRespostasValue(self,diciplina_id,valor):
        for index, resposta in enumerate(self.arestas):
            if resposta.origem == str(diciplina_id):
                self.arestas[index].valor = valor

    def __str__(self):
        return f"Competencia: {self._competencia}\nArestas: {len(self.arestas)}"
    
    def print(self):
        print(self.__str__())
        print(":[")
        for aresta in self.arestas:
            print("  {")
            aresta.print()
            print("  } \n")
        print("]")