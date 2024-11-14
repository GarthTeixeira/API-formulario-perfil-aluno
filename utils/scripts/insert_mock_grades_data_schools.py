from bson.objectid import ObjectId
from pymongo import MongoClient
from urllib.parse import quote_plus
import json
import copy
import random
import os
import argparse

dir_path = os.path.dirname(__file__)
print("Local path",dir_path)
# Configuração do argparse para receber parâmetros
parser = argparse.ArgumentParser(description="Insere escola no banco de dados - modo de alunos e notas randômicas.")

parser.add_argument("--school", type=str, default="", help="Nome da escola")

# Parse dos argumentos
args = parser.parse_args()


f_config = open('/home/garth/Documents/Projetos/API-formulario-perfil-aluno/db_resources/db_config.json')
mongo_db_infos = json.load(f_config)


connection_string = 'mongodb+srv://{}:{}@{}/?retryWrites=true&w=majority&appName=Cluster0&ssl=true'.format(
            mongo_db_infos['USERNAME'],
            quote_plus(mongo_db_infos['PASSWORD']),
            mongo_db_infos['HOST']
        )

arquivos = {}

if (args.school != ""):
    arquivos['f_disciplinas'] = open('{}/data/disciplinas.{}.json'.format(dir_path, args.school))
    arquivos['f_escolas'] = open('{}/data/escolas.{}.json'.format(dir_path, args.school))
else:
    arquivos['f_disciplinas'] = open('{}/mock/disciplinas.CEFET.json'.format(dir_path))
    arquivos['f_escolas'] = open('{}/mock/escolas.CEFET.json'.format(dir_path))

# Connect to the database

f_disciplinas, f_escolas = arquivos.values()

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
            nova_turma['ano'] = nova_turma['ano'] + serie_num -1

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

                for key in aluno['notas']['enem']:
                     aluno['notas']['enem'][key] = round(random.uniform(350, 950), 2)  # uniform gera floats no intervalo especificado

                aluno['notas']['historico_escolar'] = aluno['notas']['historico_escolar'] + novo_historico
                aluno['_id'] = ObjectId()
            novas_turmas.append(nova_turma)

    escola['turmas'] = novas_turmas



# Insert all the data into the collection
collection.insert_many(escolas)

print('Inserção realizada com sucesso!')
# Close the MongoDB connection
client.close()