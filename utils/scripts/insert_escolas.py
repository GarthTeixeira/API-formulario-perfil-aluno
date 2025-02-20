"""
Script será usado para inserir todas as escolas em um ambiente, não inserindo alunos. Primeiro passo para uma funcionalidade padrão de produção
Certifique-se que as turmas estão preenchidaas corretamente com os alunos, após a inserção crie um objeto para o histórico escolar, associando as notas as disciplinas para um aluno.
"""

from bson.objectid import ObjectId
from pymongo import MongoClient
from urllib.parse import quote_plus
import json
import copy
import os
import argparse

#Caminho Local
local_path = os.path.dirname(__file__)
print("Local path",local_path)
# Caminho relativo até "db_resources"
db_resources_path = os.path.join(local_path, '..', '..', 'db_resources')
# Normalizando o caminho
db_resources_path = os.path.abspath(db_resources_path)

parser = argparse.ArgumentParser(description="Insere escola no banco de dados.")

parser.add_argument("--school", type=str, default="", help="Nome da escola")
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
            mongo_db_infos['USER'],
            quote_plus(mongo_db_infos['PASSWORD']),
            mongo_db_infos['CLUSTER'],
            mongo_db_infos['PARAMS']
        )

f_disciplinas = open('{}/data/disciplinas.{}.json'.format(local_path, args.school))
f_escolas =  open('{}/data/escolas.{}.json'.format(local_path, args.school))

# Connect to the database
client = MongoClient(connection_string)
db = client['competencias_enem_data']
collection = db['escolas']

escola = json.load(f_escolas)
disciplinas = json.load(f_disciplinas)

result = collection.delete_one({'name':escola['name']})

series = ["1º ano", "2º ano", "3º ano"]

novas_turmas = []
escola['_id'] = ObjectId()
for disciplina in disciplinas:
    nova_disciplina = copy.deepcopy(disciplina)
    nova_disciplina['_id'] = ObjectId()
    escola['disciplinas'].append(nova_disciplina)

turmas = escola['turmas']

historicos = {}

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

        novo_historico = [
                    {
                        "disciplina_id":str(d["_id"]),
                        "disciplina_titulo":d["name"] + "-" + str(d["serie_ano"]),
                        "nota": 0
                    } 
                    for d in disciplinas_from_serie
                ]
        
        historicos[serie] = novo_historico
        novas_turmas.append(nova_turma)

escola['turmas'] = novas_turmas

# Insert all the data into the collection
shcools_inserted = collection.insert_one(escola)

print('Inserção realizada com sucesso!')
# Close the MongoDB connection
client.close()

print(historicos)
file_name = "modelo_historico.{}.json".format(args.school)

with open("./data/{}".format(file_name), "w",  encoding="utf-8") as json_file:
    json.dump(historicos, json_file,  ensure_ascii=False, indent=4) 

print("{} created!".format(file_name))