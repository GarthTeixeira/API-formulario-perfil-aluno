""" 
O script a seguir funcionam apenas em ambiente local. Para que os dados sejam carregados em produção, realize a importação do ambiente local.
*The following script works only in local environment. To load data in production import from local environment.*

Script de inserção de valores de competência:

Como os resultados dos formulários serão preenchidos por várias pessoas em um longo período de tempo, este script consegue preencher todas
as respostas de professores fakes de todas as disciplinas das turmas.

Parametros:

*
Insertion competence values script:
As the form results are filed by several people over a long period this script can fill in every fake teacher answer from every class subject.
*

"""

from bson.objectid import ObjectId
from pymongo import MongoClient
from urllib.parse import quote_plus
from bson import json_util
import json
import random
from faker import Faker
import argparse
import time
import pprint
import os
from api import post_request, put_request

def insert_resposta(list_formularios_id, list_disciplinas, list_competencias, professor):
    
    insert_resposta_url_and_payloads = []
    response = []
    form_num = len(list_formularios_id)
    print("Inserindo respostas para {} formulários".format(form_num))

    for index,form_id in enumerate(list_formularios_id):

        disciplinas_da_turma = list(filter(lambda disc: disc['serie_ano'] == index+1, list_disciplinas))
        competencias_cognitivas = list(filter(lambda comp: comp['tag']== 'COGNITIVOS', list_competencias))

        for disciplina in disciplinas_da_turma:

            competencias_by_area = list(filter(lambda comp: comp['tag'] == disciplina['area'], list_competencias))
            comp_map = {}

            for comp in competencias_by_area:
                comp_map[comp['_id']] = [random.uniform(0, 10) for _ in range(comp['competencias_habilidades'])]
            
            payload = {
                'disciplina': disciplina['_id'],
                'formulario': form_id,
                'area': disciplina['area'],
                'competencias': comp_map,
                'professor': professor
            }

            nome_diciplina = disciplina["nome"] + '-' + str(disciplina["serie_ano"])

            print('Formulario {} referente a disciplina {} possui {} competencias com professor {}'
                  .format(payload['formulario'],nome_diciplina, len(comp_map.values()), professor['nome']))

            insert_resposta_url_and_payloads.append(
                (url_insert_resposta,payload.copy())
            )

            cog_map = {}
            for comp in competencias_cognitivas:
                cog_map[comp['_id']] = [random.uniform(0, 10)]

            payload['area'] = 'COGNITIVOS'
            payload['competencias'] = cog_map


            insert_resposta_url_and_payloads.append(
                (url_insert_resposta,payload.copy())
            )


        print("Inserindo {} respostas para o formulário do professor {} índice {}/{}".format(len(insert_resposta_url_and_payloads),professor['nome'],index +1 ,form_num))

        for url,request in insert_resposta_url_and_payloads:            
            response.append(put_request(url, request))
    
    return response

#Caminho Local
local_path = os.path.dirname(__file__)
print("Local path",local_path)
# Caminho relativo até "db_resources"
db_resources_path = local_path

# Construindo o caminho para "db_resources"
for _ in range(3):
    db_resources_path = os.path.join(db_resources_path, '..')
db_resources_path = os.path.join(db_resources_path, 'db_resources')

# Normalizando o caminho
db_resources_path = os.path.abspath(db_resources_path)

parser = argparse.ArgumentParser(description="Cria formularios com valores de competências randômicas.")

parser.add_argument("--school", type=str, default="", help="Id escola")
parser.add_argument("--env", type=str, default="", help="ambiente")

# Parse dos argumentos
args = parser.parse_args()

f_config = open('{}/db_config.json'.format(db_resources_path))
config = json.load(f_config)

mongo_db_infos = config[args.env] if (args.env != "") else config['local']
school_id = config["params"]["school_id"] if (args.school == "") else args.school

if 'CLUSTER' not in mongo_db_infos:
    mongo_db_infos['CLUSTER'] = mongo_db_infos['HOST'] + ":" + mongo_db_infos['PORT']


connection_string = 'mongodb{}://{}:{}@{}/{}'.format(
            mongo_db_infos['SRV'],
            mongo_db_infos['USER_NAME'],
            quote_plus(mongo_db_infos['PASSWORD']),
            mongo_db_infos['CLUSTER'],
            mongo_db_infos['PARAMS']
        )

#Url das apis
url_insert_professor=f"http://localhost:{config["params"]["backendport"]}/professor-form/insert-professor"
url_insert_resposta = f"http://localhost:{config["params"]["backendport"]}/professor-form/insert-resposta"

#Conexão com o banco de dados MongoDB
client = MongoClient(connection_string)
db = client['competencias_enem_data']
competencias_collection = db['competencias']
escolas_collection = db['escolas']

pipeline_num_habilidades = [
    {
        '$project': {
            'descricao_area': 0
        }
    }, {
        '$set': {
            'competencias_habilidades': {
                '$cond': {
                    'if': {
                        '$ne': [
                            '$tag', 'COGNITIVOS'
                        ]
                    }, 
                    'then': {
                        '$size': {
                            '$map': {
                                'input': {
                                    '$objectToArray': '$competencias_habilidades'
                                }, 
                                'as': 'item', 
                                'in': '$$item.k'
                            }
                        }
                    }, 
                    'else': 1
                }
            },
            '_id': {
                '$toString':'$_id'
            }
        }
    }
]

pipeline_turmas = [
    {
        '$match': {
            '_id': ObjectId(school_id)
        }
    }, {
        '$project': {
            'turmas.alunos': 0, 
            'disciplinas': 0, 
            '_id': 0, 
            'nome': 0
        }
    }, {
        '$unwind': {
            'path': '$turmas'
        }
    }, {
        '$replaceRoot': {
            'newRoot': '$turmas'
        }
    }, {
        '$set':{
            '_id':  {
                '$toString': '$_id'
            },
            # 'serie_ano':{ '$toInt': { '$substrCP': ["$serie", 0, 1] } }
        }
    }, {
        '$match': {
            'nome': 'ET TURMA C'
        }
    }

]

pipeline_disciplinas = [
    {
        '$match': {
            '_id': ObjectId(school_id)
        }
    }, {
        '$project': {
            'disciplinas': 1
        }
    }, {
        '$unwind': {
            'path': '$disciplinas'
        }
    }, {
        '$replaceRoot': {
            'newRoot': '$disciplinas'
        }
    }, {
        '$set': {
            '_id': {
                '$toString': '$_id'
            }
        }
    }, {
        '$project': {
            'codigoBNCC': 0
        }
    }
]



list_competencias =  list(competencias_collection.aggregate(pipeline_num_habilidades))
list_turmas = list(escolas_collection.aggregate(pipeline_turmas))
list_disciplinas = list(escolas_collection.aggregate(pipeline_disciplinas))
school = escolas_collection.find_one({"_id":ObjectId(school_id)},{"disciplinas":0})

# Verificar as listas
# print("Competências:")
# pprint.pprint(list_competencias)
# print("Turmas:")
# pprint.pprint(list_turmas)
# print("Disciplinas:")
# pprint.pprint(list_disciplinas)
# print("Escola:")
# pprint.pprint(school)


#TODO: isolate these codes lines in fuctions
form_ids = []
turma_form_dict = {}

print(url_insert_professor)

school['turmas'] = list_turmas
school['id'] = str(school['_id'])
del school['_id']

payload_insert_professor = {
    'nome': Faker().name(),
    'email': Faker().email(),
    'escola': school,
    'telefone': Faker().phone_number()
}

response = post_request(url_insert_professor, payload_insert_professor)

# Verificar resposta de inserção do professor
# print('resposta',response)

forms_ids = list(map(lambda form: form['id'], response))
teatcher = {
    'nome': response[0]['professor']['nome'],
    'email': response[0]['professor']['email'],
}


insert_resposta(forms_ids, list_disciplinas, list_competencias, teatcher)