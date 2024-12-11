# API-formulario-perfil-aluno

Form API to collect high-school students skills/competences data of ENEM (Brazil's Nacional Entrance Exam) for further analysis. *Api para formulário dos alunos do ensino médio para estudos de suas competências para o ENEM*

## Requriments
- python 3.12.6

## Installation *Instalação*

1. Make sure you have `pip` installed. If not, follow the instructions below to install it. *Tenha certeza que o `pip` está instalado. Se não execute a instrução de  código abaixo para instala-lo.*

    ```bash
    $ sudo apt install python3-pip
    ```
- (Optinal) Is very recomended that you use an vitural enviroment, to no compromise your system with intaling the packages, for that use the following command to create it.

    ```bash
    $ python3 -m venv .env
    ```
    and the next to active
    
    ```bash
    $ source .env/bin/active
    ```

2. Install the required dependencies by running the following command. *Instale as dependências necessárias executando o comando*:

    ```bash
    $ pip install -r requirements.txt
    ```

    This will install all the necessary packages specified in the `requirements.txt` file.

3. Other dependencies for plot graphs. *Instale dependências para os plot dos grafos.*

    ```bash
    $ pip install networkx
    $ pip install matplotlib
    $ python -m pip install PyQt5
    ```

## Create database locally (optional)  *Criar base de dados localmente(opcional)*

1 - Execute the docker-compose file on your directory navigate to `db_resources` folder  *Executar o arquivo docker-compose no seu diretório, navegue até a pasta `db_resources`*
```bash
$ docker-compose up
```
2 - Use the scripts located in `mock` directory to insertions and tests *Use os scripts localizados no diretório `mock` para inserções e testes*

```bash
$ python /utils/scripts/<insert-script>
```
> [!IMPORTANT]
> In case to use your own data model of school or subjects insert your model on `data` directory (created by you), located in `scripts` directory
> *Caso queira utilizara algum modelo de escola ou disciplina, modificar o exemplo e adicionar no diretório `data` (criado por você), dentro do diretório `scripts`*


## Running *Excutar o programa*

1. Running by using command

```bash
$ python3 main.py    
```

> [!IMPORTANT]
> Before running the server, make sure to check if the IP address of the machine where the server is running is added to the database for connection.
> *Caso esteja acessando o ambiente de produção remotamente, antes de executar o servidor, certifique-se de verificar se o endereço IP da máquina onde o servidor está rodando foi adicionado ao banco de dados para conexão.*  


> [!NOTE]  
> Find ways to host application to doesn't need run locally
> Check access of users are running locally