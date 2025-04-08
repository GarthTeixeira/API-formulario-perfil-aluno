class Escola:
    def __init__(self, id ,nome):
        self.__id = id
        self.__nome = nome

    def getEscolaId(self):
        return self.__id
    
    def to_dict(self):
        return {
            "id": self.__id,
            "nome": self.__nome,
        }
    