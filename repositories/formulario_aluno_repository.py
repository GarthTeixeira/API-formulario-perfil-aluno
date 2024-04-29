from .base_repository import BaseRepository

class FormularioAlunoRepository(BaseRepository):
    def __init__(self,connection):
        super().__init__(connection,"formulario_alunos_collection")

    # Add your custom repository methods here

    def get_by_aluno_data(self, aluno_id):
        aluno_query = self._connection.find_one({"aluno": {"_id": aluno_id}})
        return aluno_query
    
    def insert_formulario(self, formulario_data)->str:
        print(self._collection_name)
        formulario_query = self.insert_one(formulario_data)
        return formulario_query
    
    def update_formulario(self, formulario_data):
        formulario_query = self._connection.update_one({"_id": formulario_data["_id"]}, {"$set": formulario_data})
        return formulario_query