import requests

def fazer_chamada_api():
    post_url = "https://api.exemplo.com/dados"  # Substitua pela URL da API de destino

    try:
        # Fazer chamada HTTP POST
        
        payload = {"key": "value"}  # Substitua pelos dados que você deseja enviar
        response = requests.post(post_url, json=payload)
        response.raise_for_status()  # Verifica se a resposta da API foi bem-sucedida
        # Faça algo com a resposta da API de destino
        
    except requests.exceptions.RequestException as e:
        print("Ocorreu um erro ao fazer a chamada para a API:", e)

fazer_chamada_api()