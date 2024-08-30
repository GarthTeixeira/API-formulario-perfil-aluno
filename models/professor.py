class Professor:
    def __init__(self, nome, email,escola,turma):
        self.nome = nome
        self.email = email
        self.escola = escola
        self.turma = turma

    def exibir_informacoes(self):
        print(f"Nome: {self.nome}")
        print(f"E-mail: {self.email}")
        print(f"Escola: {self.escola}")
        print(f"Turma: {self.turma}")

    def to_dict(self):
        return {
            "nome": self.nome,
            "email": self.email,
            "escola": self.escola,
            "turma": self.turma
        }