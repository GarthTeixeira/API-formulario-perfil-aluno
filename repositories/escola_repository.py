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
        data = collection.find({},{"name":1})
        response = list(data)
        
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