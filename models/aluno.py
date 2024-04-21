class Aluno:
    def __init__(self, nome, idade, matricula, anos_letivos, email):
        self.nome = nome
        self.idade = idade
        self.matricula = matricula
        self.anos_letivos = anos_letivos
        self.email = email
        self.serie_atual = ''

    def exibir_informacoes(self):
        print(f"Nome: {self.nome}")
        print(f"Idade: {self.idade}")
        print(f"Matrícula: {self.matricula}")
        print(f"Série atual: {self.serie_atual}")
        print(f"E-mail: {self.email}")