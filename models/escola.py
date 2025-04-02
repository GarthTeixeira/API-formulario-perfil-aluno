class Escola:
    def __init__(self, id ,nome, turmas):
        self.__id = id
        self.__nome = nome
        self.__turmas = turmas

    def getEscolaId(self):
        return self.__id
    
    def to_dict(self):
        return {
            "id": self.__id,
            "nome": self.__nome,
            "turmas": self.__turmas,
        }
    