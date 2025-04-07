from bson.objectid import ObjectId
from pymongo import MongoClient
from urllib.parse import quote_plus
import json
import copy
from faker import Faker
import os
import argparse

#Caminho Local
local_path = os.path.dirname(__file__)
print("Local path",local_path)
# Caminho relativo até "db_resources"
db_resources_path = os.path.join(local_path, '..', '..', 'db_resources')
# Normalizando o caminho
db_resources_path = os.path.abspath(db_resources_path)

parser = argparse.ArgumentParser(description="Anonimiza alunos no banco de dados.")
parser.add_argument("--env", type=str, default="", help="ambiente")

# Parse dos argumentos
args = parser.parse_args()
f_config = {}

f_config = open('{}/db_config.json'.format(db_resources_path))
mongo_db_infos = json.load(f_config)

mongo_db_infos = mongo_db_infos[args.env]

if 'CLUSTER' not in mongo_db_infos:
    mongo_db_infos['CLUSTER'] = mongo_db_infos['HOST'] + ":" + mongo_db_infos['PORT']

connection_string = 'mongodb{}://{}:{}@{}/{}'.format(
            mongo_db_infos['SRV'],
            mongo_db_infos['USER_NAME'],
            quote_plus(mongo_db_infos['PASSWORD']),
            mongo_db_infos['CLUSTER'],
            mongo_db_infos['PARAMS']
        )

client = MongoClient(connection_string)
db = client['competencias_enem_data']
collection = db['escolas']

aggregation = [
    {
        '$match': {
            '_id': ObjectId('67ca3ac792251c0cba3d7310')
        }
    }, {
        '$unwind': '$disciplinas'
    }, {
        '$set': {
            'disciplinas._id': {
                '$toString': '$disciplinas._id'
            }
        }
    }, {
        '$group': {
            '_id': {
                'docId': '$_id', 
                'serie': '$disciplinas.serie_ano'
            }, 
            'disciplinas': {
                '$push': '$disciplinas'
            }, 
            'outrosCampos': {
                '$first': '$$ROOT'
            }
        }
    }, {
        '$project': {
            '_id': '$_id', 
            'nome': '$outrosCampos.nome', 
            'series': {
                'ano': '$_id.serie', 
                'disciplinas': '$disciplinas'
            }
        }
    }, {
        '$group': {
            '_id': '$_id.docId', 
            'series': {
                '$push': '$series'
            }, 
            'nome': {
                '$first': '$nome'
            }
        }
    }, {
        '$project': {
            'series.ano': 1, 
            'series.disciplinas.nome': 1, 
            'series.disciplinas._id': 1, 
            'nome': 1
        }
    }, {
        '$addFields': {
            'series.disciplinas.nota': 0
        }
    }
]
documentos = list(collection.aggregate(aggregation))

arqvs = []

for doc in documentos:
    element = {"nome":doc['nome'] , 'historico':{}}
    for serie in doc['series']:
        key = "{}º ano".format(serie['ano'])
        value = serie['disciplinas']
        element['historico'][key] = value
    arqvs.append(element)

with open("./data/historicos_modelo.json", "w",  encoding="utf-8") as json_file:
    json.dump(arqvs, json_file,  ensure_ascii=False, indent=4) 
print(arqvs)
