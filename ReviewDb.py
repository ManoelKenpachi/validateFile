import psycopg2
from flask import Flask, request
import hashlib
from Auth import verify_token
from HashFile import get_file_zip

class PostgresAPI:
    def __init__(self, host, port, database, user, password):
        """
        Classe que encapsula a conexão e operações com um banco de dados PostgreSQL.

        Parâmetros:
        - host: o endereço do host onde o banco de dados está localizado
        - port: a porta utilizada para a conexão com o banco de dados
        - database: o nome do banco de dados
        - user: o nome de usuário para autenticação no banco de dados
        - password: a senha para autenticação no banco de dados
        """
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        """
        Estabelece a conexão com o banco de dados PostgreSQL.
        """
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print("Connected to the PostgreSQL database!")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)

    def close_connection(self):
        """
        Fecha a conexão com o banco de dados PostgreSQL.
        """
        if self.connection:
            self.connection.close()
            print("PostgreSQL connection closed.")

    def execute_select(self, query):
        """
        Executa uma consulta SELECT no banco de dados PostgreSQL.

        Parâmetros:
        - query: a consulta SELECT a ser executada

        Retorna:
        - Uma lista de hashes, onde cada hash representa uma linha da consulta.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]

            return result
        except (Exception, psycopg2.Error) as error:
            print("Error while executing SELECT query:", error)

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data(token = ''):
    """
    Função de endpoint que retorna os dados do banco de dados PostgreSQL como JSON.

    Retorna:
    - Uma resposta JSON contendo os dados retornados da consulta SELECT.
    """
    token = request.get_json()['token']
    if verify_token(token):
        postgres = PostgresAPI(
            host='localhost',
            port=5432,
            database='Lojas',
            user='postgres',
            password='mysecretpassword'
        )
        postgres.connect()
        select = postgres.execute_select('Select id, name from public.dados d ')
        list_hash = []

        for line in select:
            line_str = ','.join([str(line['id']), line['name']])
            list_hash.append(hashlib.md5(str(line_str).encode()).hexdigest())

        postgres.close_connection()
        
        return list_hash
    else:
        return {'Error': 'databse off'}    
    
@app.route('/file', methods=['GET'])
def get_file():
    """
    Função de endpoint que retorna os dados de um arquivo CSV zipado.

    Retorna:
    - Uma resposta JSON contendo os dados retornados do arquivo.
    """

    file = request.get_json()['file']
    path = request.get_json()['path']

    hashs = get_file_zip(file, path)

    return hashs

@app.route('/validate', methods=['GET'])
def validate():

    token = request.get_json()['token']
    file = get_file()

    #Removendo cabeçalho
    del file[0]

    data = get_data(token)

    new_itens = []

    for line in file:
        if line in data:
            continue
        else:
            new_itens.append(line)
            
    return new_itens
        
if __name__ == '__main__':
    app.run()