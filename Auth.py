from flask import Flask, request, jsonify
from passlib.hash import pbkdf2_sha256
import psycopg2
import jwt
from datetime import datetime, timedelta

from flask_cors import CORS

def verificar_data_maior(data1: str, data2: str, formato: str) -> str:
    try:
        dt1 = datetime.strptime(data1, formato)
        dt2 = datetime.strptime(data2, formato)

        if dt1 < dt2:
            return True
        elif dt2 > dt1:
            return {'Erro': "Token Expirado"}
        else:
            return {'Erro': "As datas são iguais"}

    except ValueError:
        return {'Erro': "Formato de data inválido"}


app = Flask(__name__)
app.config['SECRET_KEY'] = 'pintamanhagaba'
CORS(app) 

DB_NAME = 'Lojas'
DB_USER = 'postgres'
DB_PASSWORD = 'mysecretpassword'
DB_HOST = 'localhost'
DB_PORT = '5432'

# Função para criar a conexão com o banco de dados
def create_connection():
    connection = psycopg2.connect(
    host=DB_HOST,
    port=5432,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
    return connection

# Rota para registro de usuários
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Criptografando a senha usando PBKDF2
    hashed_password = pbkdf2_sha256.hash(password)

    # Inserindo o usuário no banco de dados
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
    connection.commit()
    connection.close()

    return jsonify({'message': 'Registro realizado com sucesso!'})

# Rota para login de usuários
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    connection = create_connection()

    cursor = connection.cursor()
    hashed_password = pbkdf2_sha256.hash(password)

    try:
        cursor.execute(f"""SELECT password FROM users WHERE username = '{username}'""")

        result = cursor.fetchone()
        connection.close()

        if result is None:
            return jsonify({'message': 'Usuário não encontrado!'})

        hashed_password = result[0]
        # return {'username': username, 'pass': f"{result}, {hashed_password}'"""}

        if pbkdf2_sha256.verify(password, hashed_password):
            # Gerando um token temporário válido por 30 minutos
            token = jwt.encode({'username': f'{username}', 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
            return jsonify({'token': token})
        else:
            return jsonify({'message': 'Credenciais inválidas!'})
    except Exception as e:
        return {'error': f'{e}'}

# Função para verificar a validade do token
def verify_token(token: str) -> bool:

    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        token_expiracao = payload.get('exp')

        if token_expiracao:
            expiracao = datetime.fromtimestamp(token_expiracao)
            agora = datetime.now()
            # return {'agora': f'{agora}', 'expirado': f'{expiracao}'}

            date = verificar_data_maior(str(agora).split('.')[0], str(expiracao).split('.')[0], "%Y-%m-%d %H:%M:%S")

            if date:
                return True  # Token é válido, não expirou
            else:
                return {'Erro':'Token Expirado'}   # Token expirou

        return {'Erro':'Token não contém informação de expiração'} # Token não contém informação de expiração

    except jwt.ExpiredSignatureError:
        return {'Erro':'Token Expirado'}   # Token expirou

    except jwt.InvalidTokenError:
        return {'Erro':'Token inválido'}   # Token inválido
    
    except Exception as e:
        return {'Erro': f'{e}'}

# Rota para verificar se o token é válido
@app.route('/verify', methods=['POST'])
def verify():

    data = request.get_json()
    token = data['token'] 

    if not token:
        return jsonify({'message': 'Token não fornecido!'}), 401    

    username = verify_token(token)

    if username:
        # Gerando um novo token válido por 1 dia
        new_token = jwt.encode({'username': username, 'exp': datetime.utcnow() + timedelta(days=1)}, app.config['SECRET_KEY'])

        return jsonify({'token': new_token})
    else:
        return jsonify({'message': 'Token inválido!'}), 401

if __name__ == '__main__':
    app.run(port=5001)
