class Aluno:
    def __init__(self, nome, matricula, anos_letivos, email, escola, serie = '', idade = None):
        self.nome = nome
        self.idade = idade
        self.matricula = matricula
        self.anos_letivos = anos_letivos
        self.email = email
        self.serie = serie
        self.escola = escola

    def exibir_informacoes(self):
        print(f"Nome: {self.nome}")
        print(f"Idade: {self.idade}")
        print(f"Matrícula: {self.matricula}")
        print(f"Anos letivos: {self.anos_letivos}")
        print(f"Escola: {self.escola}")
        print(f"Série atual: {self.serie}")
        print(f"E-mail: {self.email}")

    def to_dict(self):
        return {
            "nome": self.nome,
            "idade": self.idade,
            "matricula": self.matricula,
            "anos_letivos": self.anos_letivos,
            "email": self.email,
            "serie": self.serie,
            "escola": self.escola
        }