from .base_repository import BaseRepository

class FormularioAlunoRepository(BaseRepository):
    def __init__(self,connection):
        super().__init__(connection,"formulario_alunos_collection")

    # Add your custom repository methods here
    
    def insert_formulario(self, formulario_data)->str:
        formulario_query = self.insert_one(formulario_data)
        return formulario_query
    
    def update_formulario(self, formulario_data):
        formulario_query = self._connection.update_one({"_id": formulario_data["_id"]}, {"$set": formulario_data})
        return formulario_query
    
    def get_by_school_id(self, school_id):
        collection = self._connection.get_collection(self._collection_name)
        response = collection.find( {"professor.escola": school_id}, {"grafos":0})
        return list(response)