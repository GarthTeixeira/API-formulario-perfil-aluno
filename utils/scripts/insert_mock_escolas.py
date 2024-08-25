from bson.objectid import ObjectId
from pymongo import MongoClient
from urllib.parse import quote_plus
import json
import copy

f_config = open('../../db_resources/db_config.json')
mongo_db_infos = json.load(f_config)


connection_string = 'mongodb+srv://{}:{}@{}/?retryWrites=true&w=majority&appName=Cluster0&ssl=true'.format(
            mongo_db_infos['USERNAME'],
            quote_plus(mongo_db_infos['PASSWORD']),
            mongo_db_infos['HOST']
        )

f_disciplinas = open('../mock/disciplinas.json')
f_escolas = open('../mock/escolas.json')

# Connect to the database
client = MongoClient(connection_string)
db = client['competencias_enem_data']
collection = db['escolas']

escolas = json.load(f_escolas)
disciplinas = json.load(f_disciplinas)

series = ["1º ano", "2º ano", "3º ano"]

for escola in escolas:
    novas_turmas = []
    escola['_id'] = ObjectId()
    for disciplina in disciplinas:
        disciplina['_id'] = ObjectId()
        escola['disciplinas'].append(disciplina)
    
    turmas = escola['turmas']

    for turma in turmas:
        for serie in series:
            nova_turma = copy.deepcopy(turma)
            nova_turma["serie"] = serie
            nova_turma['_id'] = ObjectId()
            novas_turmas.append(nova_turma)

    escola['turmas'] = novas_turmas



# Insert all the data into the collection
collection.insert_many(escolas)

# Close the MongoDB connection
client.close()