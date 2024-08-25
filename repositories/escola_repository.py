from bson.objectid import ObjectId
from .base_repository import BaseRepository
from typing import Dict, List

class EscolaRepository(BaseRepository):
    def __init__(self, connection):
        super().__init__(connection, "escolas")
        
       
    def get_school_by_id_and_subjects_by_area(self,school, area):
        collection = self._connection.get_collection(self._collection_name)
        pipeline = [
            # Match the school by id
            { "$match": { "_id": ObjectId(school) } },

            # Filter the disciplinas array to only include subdocuments with area "EXATAS"
            { 
                "$addFields": {
                    "disciplinas": {
                        "$filter": {
                            "input": "$disciplinas",
                            "as": "disciplina",
                            "cond": { "$eq": ["$$disciplina.area", area] }
                        }
                    }
                }
            }
        ]
        data = collection.aggregate(pipeline)
        response = list(data)
        
        return response
    
    
    def get_shchools_names(self):
        collection = self._connection.get_collection(self._collection_name)
        pipeline = [{"$project": {"name": 1,"turmas.nome": 1, "turmas.serie": 1, "turmas._id": 1}}]
                    # Execute the aggregation
         # Execute the aggregation
        results = collection.aggregate(pipeline)
        response = []

        for doc in results:
            # Converte o _id da escola para string
            doc["_id"] = str(doc["_id"])
            
            # Converte os _id's das turmas para string
            if "turmas" in doc:
                for turma in doc["turmas"]:
                    if "_id" in turma:
                        turma["_id"] = str(turma["_id"])
            
            response.append(doc)
        
        return response
    
    def get_school_and_disciplina_by_id(self,school_id, disciplina_id):
        collection = self._connection.get_collection(self._collection_name)
        pipeline = [
            # Match the school by id
            { "$match": { "_id": ObjectId(school_id) } },

            # Filter the disciplinas array to only include subdocuments with area "EXATAS"
            { 
                "$addFields": {
                    "disciplinas": {
                        "$filter": {
                            "input": "$disciplinas",
                            "as": "disciplina",
                            "cond": { "$eq": ["$$disciplina._id", ObjectId(disciplina_id)] }
                        }
                    }
                }
            }
        ]

        data = collection.aggregate(pipeline)
        response = list(data)
        
        return response
    
    def get_school_disciplinas(self, school_id):
        collection = self._connection.get_collection(self._collection_name)
        pipeline = [
            { "$match": { "_id": ObjectId(school_id) } },

            {
                "$project":{
                    "_id":1,
                    "disciplinas":{
                        "$map": {
                            "input": "$disciplinas",
                            "as": "disciplina",
                                "in": {
                                    "_id": "$$disciplina._id",
                                    "name": "$$disciplina.name",
                                    "serie_ano": "$$disciplina.serie_ano"
                                }
                        }
                    }
                }
            }
           
            ]
        
        response = collection.aggregate(pipeline)
        return list(response)
    
    
    def get_school_classes(self, school_id):
        collection = self._connection.get_collection(self._collection_name)
        pipeline = [
            # Match the school by id
            { "$match": { "_id": ObjectId(school_id) } },

            # Filter the disciplinas array to only include subdocuments with area "EXATAS"
            {
                "$project": {
                "_id": 1,  # Exclude the _id field from the output
                "turmas": {
                    "$map": {
                        "input": "$turmas",
                        "as": "turma",
                        "in": {
                            "nome": "$$turma.nome",
                            "serie_ano": "$$turma.serie"
                        }
                    }
                }
                }
            }
        ]
        response = collection.aggregate(pipeline)
        
        return list(response)
    
    def get_school_by_id_and_subjects_by_area_and_serie_ano(self,school, serie_ano, area = ''):
        collection = self._connection.get_collection(self._collection_name)
        condition = {}
        if(area == ''):
            condition = {"$eq": ["$$disciplina.serie_ano", serie_ano] }
        else:
            condition = { "$and":[{"$eq": ["$$disciplina.area", area] },{"$eq": ["$$disciplina.serie_ano", serie_ano] }]}
        
        pipeline = [
            # Match the school by id
            { "$match": { "_id": ObjectId(school) } },

            # Filter the disciplinas array to only include subdocuments with area "EXATAS"
            { 
                "$addFields": {
                    "disciplinas": {
                        "$filter": {
                            "input": "$disciplinas",
                            "as": "disciplina",
                            "cond": condition
                        }
                    }
                }
            }
        ]
        data = collection.aggregate(pipeline)
        response = list(data)
        
        return response