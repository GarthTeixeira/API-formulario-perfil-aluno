class Resposta:
    def __init__(self, origem, valor, destino = []) :
        self.origem = origem
        self.valor = valor
        self.destino = destino

    def __str__(self):
        return f"Disciplina de origem: {self.origem}\nValor: {self.valor}\nDisciplina de destino: {self.destino}"
    
    def print(self):
        print(self.__str__())

    def to_dict(self):
        return {
            "origem": self.origem,
            "valor": self.valor,
            "destino": self.destino
        }