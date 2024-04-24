from .base_repository import BaseRepository

class FormularioAlunoRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    # Add your custom repository methods here

    def get_by_aluno_data(self, aluno_data):
        aluno_query = self._connection.find_one({"matricula": aluno_data["matricula"], "email": aluno_data["email"], 
                                               "escola": aluno_data["escola"]})
        return aluno_query
    
    def insert_formulario(self, formulario_data):
        formulario_query = self._connection.insert_one(formulario_data)
        return formulario_query
    
    def update_formulario(self, formulario_data):
        formulario_query = self._connection.update_one({"_id": formulario_data["_id"]}, {"$set": formulario_data})
        return formulario_query