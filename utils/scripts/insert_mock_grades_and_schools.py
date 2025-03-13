""" 
O script a seguir funcionam apenas em ambiente local. Para que os dados sejam carregados em produção, realize a importação do ambiente local.
*The following script works only in local environment. To load data in production import from local environment.*

Script de inserção de valores de nota:
Este script insere uma escola que contém alunos que não possuem notas, atribuindo notas aleatórias para os alunos. O script também extende as turmas,
no mock carregado o estudante contém apenas a turma inicial de 1° ano, este script cria para o mesmo turmas dos anos seguintes.

*
Insertion grade values script:
This script inserts a school containing students without grades assigning random grade values to every student. The script also extends the classes,
on the loaded mock file the student is only included in the first high school class year, this script creates the following years for it.
*

"""
from bson.objectid import ObjectId
from pymongo import MongoClient
from urllib.parse import quote_plus
import json
import copy
import random
import os
import argparse

#Caminho Local
local_path = os.path.dirname(__file__)
print("Local path",local_path)
# Caminho relativo até "db_resources"
db_resources_path = os.path.join(local_path, '..', '..', 'db_resources')
# Normalizando o caminho
db_resources_path = os.path.abspath(db_resources_path)

parser = argparse.ArgumentParser(description="Insere escola no banco de dados - modo de alunos e notas randômicas.")

parser.add_argument("--school", type=str, default="", help="Nome do arquivo da escola")
parser.add_argument("--env", type=str, default="", help="ambiente")

# Parse dos argumentos
args = parser.parse_args()
f_config = {}

f_config = open('{}/db_config.json'.format(db_resources_path))
config = json.load(f_config)
mongo_db_infos = config[args.env]

if 'CLUSTER' not in mongo_db_infos:
    mongo_db_infos['CLUSTER'] = mongo_db_infos['HOST'] + ":" + mongo_db_infos['PORT']


connection_string = 'mongodb{}://{}:{}@{}/{}'.format(
            mongo_db_infos['SRV'],
            mongo_db_infos['USER'],
            quote_plus(mongo_db_infos['PASSWORD']),
            mongo_db_infos['CLUSTER'],
            mongo_db_infos['PARAMS']
        )

arquivos = {}

if (args.school != ""):
    arquivos['f_disciplinas'] = open('{}/data/disciplinas.{}.json'.format(local_path, args.school))
    arquivos['f_escolas'] = open('{}/data/escolas.{}.json'.format(local_path, args.school))
else:
    arquivos['f_disciplinas'] = open('{}/mock/disciplinas.ET.json'.format(local_path))
    arquivos['f_escolas'] = open('{}/mock/escolas.ET.json'.format(local_path))

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
    escola['_id'] = ObjectId(config['params']['school_id']) if len(escolas) ==1 else ObjectId()
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
                        "nota": round(random.uniform(6, 10), 1)
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