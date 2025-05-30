import subprocess

def run_docker_compose():
    try:
        # Change directory to db_resources
        subprocess.run(["docker", "compose", "up" ], cwd="db_resources", check=True)
        print("✅ Docker Compose executado com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar Docker Compose: {e}")
    except FileNotFoundError:
        print("Comando Docker Compose não foi encontrado. Verifique seu caminho.")

if __name__ == "__main__":
    run_docker_compose()