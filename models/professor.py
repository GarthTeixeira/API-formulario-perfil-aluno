class Professor:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email
        self.disciplinas = []

    def exibir_informacoes(self):
        print(f"Nome: {self.nome}")
        print(f"E-mail: {self.email}")


    def to_dict(self):
        return {
            "nome": self.nome,
            "email": self.email,
        }