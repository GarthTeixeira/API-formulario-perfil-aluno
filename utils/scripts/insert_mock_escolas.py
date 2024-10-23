from bson.objectid import ObjectId
from pymongo import MongoClient
from urllib.parse import quote_plus
import json
import copy
import random
import os

print("Current Working Directory:", os.getcwd())

f_config = open('/home/garth/Documents/Projetos/API-formulario-perfil-aluno/db_resources/db_config.json')
mongo_db_infos = json.load(f_config)


connection_string = 'mongodb+srv://{}:{}@{}/?retryWrites=true&w=majority&appName=Cluster0&ssl=true'.format(
            mongo_db_infos['USERNAME'],
            quote_plus(mongo_db_infos['PASSWORD']),
            mongo_db_infos['HOST']
        )

f_disciplinas = open('{}/utils/mock/disciplinas.json'.format(os.getcwd()))
f_escolas = open('{}/utils/mock/escolas.json'.format(os.getcwd()))

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
        nova_disciplina = copy.deepcopy(disciplina)
        nova_disciplina['_id'] = ObjectId()
        escola['disciplinas'].append(nova_disciplina)
    
    turmas = escola['turmas']
    

    for turma in turmas:
        for serie in series:
            nova_turma = copy.deepcopy(turma)
            nova_turma["serie"] = serie
            nova_turma['_id'] = ObjectId()
            serie_num = int(serie[0])

            disciplinas_from_serie = list(filter(
                lambda disciplina: disciplina['serie_ano'] == serie_num,
                escola['disciplinas']
            ))

            for aluno in nova_turma['alunos']:
                ## Generate random grade for student and add to scholar historic
                novo_historico = [
                    {
                        "disciplina_id":d["_id"],
                        "disciplina_titulo":d["name"] + "-" + str(d["serie_ano"]),
                        "nota": round(random.uniform(0, 10), 1)
                    } 
                    for d in disciplinas_from_serie
                ]
                aluno['notas']['historico_escolar'] = aluno['notas']['historico_escolar'] + novo_historico

            novas_turmas.append(nova_turma)

    escola['turmas'] = novas_turmas



# Insert all the data into the collection
collection.insert_many(escolas)

print('Inserção realizada com sucesso!')
# Close the MongoDB connection
client.close()