class Professor:
    def __init__(self, nome, email,telefone="" , disciplinas = []):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.disciplinas = disciplinas

    def exibir_informacoes(self):
        print(f"Nome: {self.nome}")
        print(f"E-mail: {self.email}")
        print(f"Telefone: {self.telefone}")


    def to_dict(self):
        return {
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "disciplinas": self.disciplinas
        }