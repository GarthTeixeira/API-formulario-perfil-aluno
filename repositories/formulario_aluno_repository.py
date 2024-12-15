from .base_repository import BaseRepository
from bson.objectid import ObjectId

class FormularioAlunoRepository(BaseRepository):
    def __init__(self,connection):
        super().__init__(connection,"formularios_professor")

    # Add your custom repository methods here
    
    def insert_formulario(self, formulario_data)->str:
        formulario_query = self.insert_one(formulario_data)
        return formulario_query
    
    def update_formulario(self, formulario_data):
        formulario_query = self.update_one(formulario_data["_id"], formulario_data)
        if (formulario_query.raw_result['n'] == 1):
            return str(formulario_data["_id"])
        else :
            return ''

    
    def get_by_school_id(self, school_id):
        collection = self._connection.get_collection(self._collection_name)
        response = collection.find( {"escola": school_id}, {"grafos":0})
        return list(response)
    
    def get_teacher_by_school_id(self, school_id):
        collection = self._connection.get_collection(self._collection_name)

        pipeline = [
            {
                '$match': {
                    'escola': school_id
                }
            }, {
                '$project': {
                    'turma': 1, 
                    'professores': 1, 
                    'formulario': '$_id', 
                    '_id': 0
                }
            }, {
                '$unwind': {
                    'path': '$professores'
                }
            }, {
                '$project': {
                    'nome': '$professores.nome', 
                    'email': '$professores.email', 
                    'turma': 1, 
                    'formulario': {
                        '$toString': [
                            '$formulario'
                        ]
                    }
                }
            }
        ]
        return list(collection.aggregate(pipeline))
        
    def get_by_school_and_turma(self,school,turma):
        collection = self._connection.get_collection(self._collection_name)

        pipeline = [
            {
                "$match":{
                    "escola":school,
                    "turma":turma
                }
            }
        ]

        response = list(collection.aggregate(pipeline))
        return response
    
    def get_subject_teatchers_registers(self,form_id):
        collection = self._connection.get_collection(self._collection_name)

        pipeline = [
            {
                '$match': {
                    '_id': ObjectId(form_id)
                }
            }, {
                '$project': {
                    'professores': 1
                }
            }, {
                '$unwind': {
                    'path': '$professores'
                }
            }, {
                '$replaceRoot': {
                    'newRoot': '$professores'
                }
            }, {
                '$unwind': {
                    'path': '$disciplinas'
                }
            }, {
                '$project': {
                    'nome': 1, 
                    'email': 1, 
                    'tipo': '$disciplinas.tipo', 
                    'ultima_resposta': '$disciplinas.data_resposta', 
                    'disciplina': '$disciplinas.disciplina'
                }
            }, {
                '$group': {
                    '_id': '$disciplina', 
                    'register': {
                        '$addToSet': {
                            'ultima_resposta': '$ultima_resposta', 
                            'tipo': '$tipo', 
                            'professor': '$nome'
                        }
                    }
                }
            }, {
                '$set': {
                    '_id': '$_id.id', 
                    'nome': '$_id.nome'
                }
            }
        ]

        response = list(collection.aggregate(pipeline))
        return response