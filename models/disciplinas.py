class Disciplina:
    def __init__(self, nome, codigo, ano_serie,area,escola):
        self.nome = nome
        self.codigo = codigo
        self.ano_serie = ano_serie,
        self.area = area
        self.escola = escola

    def __str__(self):
        return f"Disciplina: {self.nome}\nCódigo: {self.codigo}"