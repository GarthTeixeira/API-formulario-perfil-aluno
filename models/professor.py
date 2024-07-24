class Professor:
    def __init__(self, nome, email,ano_escolar,escola_id,turma):
        self.ano_escolar = ano_escolar
        self.nome = nome
        self.email = email
        self.escola_id = escola_id
        self.turma = turma

    def exibir_informacoes(self):
        print(f"Nome: {self.nome}")
        print(f"E-mail: {self.email}")
        print(f"Ano escolar: {self.ano_escolar}")
        print(f"Escola: {self.escola_id}")
        print(f"Turma: {self.turma}")

    def to_dict(self):
        return {
            "nome": self.nome,
            "email": self.email,
            "ano_escolar": self.ano_escolar,
            "escola": self.escola_id,
            "turma": self.turma
        }