from base_repository import BaseRepository

class FormularioAlunoRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    # Add your custom repository methods here

    def get_by_aluno_data(self, aluno_data):
        aluno_query = self._db.aluno.find_one({"matricula": aluno_data["matricula"], "email": aluno_data["email"], 
                                               "escola": aluno_data["escola"]})
        return aluno_query