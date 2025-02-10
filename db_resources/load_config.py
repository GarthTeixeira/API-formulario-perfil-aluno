import json
from dotenv import load_dotenv
import os

# Carrega o arquivo .env localmente
load_dotenv() 

# Função para carregar configurações de um arquivo JSON
def load_config(json_path="db_resources/db_config.json"):
    # Configurações padrão (caso o arquivo não exista)
    default_config = {
        "HOST": "",
        "PORT": "",
        "SRV": "",
        "USER": "",
        "PASSWORD": "",
        "DB_NAME": "",
        "PARAMS": ""
    }

    if os.path.exists(json_path):
        try:
            with open(json_path, "r") as file:
                config = json.load(file)[os.getenv("FLASK_ENV")]
        except Exception as e:
            print(f"Erro ao carregar o arquivo de configuração: {e}")
            config = {}
    else:
        print(f"Arquivo de configuração não encontrado: {json_path}")
        config = {}
    
    # Mescla as configurações padrão com as do arquivo JSON
    config = {**default_config, **config}

    # Sobrescrever variáveis com valores do ambiente, se definidos
    host = os.getenv("HOST", config["HOST"])
    port = os.getenv("PORT", config["PORT"])

    config["CLUSTER"] = os.getenv("CLUSTER",host+":"+port)
    config["SRV"] = os.getenv("SRV", config["SRV"])
    config["USER"] = os.getenv("USER", config["USER"])
    config["PASSWORD"] = os.getenv("PASSWORD", config["PASSWORD"])
    config["DB_NAME"] = os.getenv("DB_NAME", config["DB_NAME"])
    config["PARAMS"] = os.getenv("PARAMS", config["PARAMS"])

    return config

