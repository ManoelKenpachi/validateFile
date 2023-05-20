# Passo 1: Executando o Docker com PostgreSQL
docker run --name postgres-db -e POSTGRES_PASSWORD=minhasenha -p 5432:5432 -d postgres

# Passo 2: Criando o Banco de Dados "Lojas"
docker exec -it postgres-db psql -U postgres
# Digite a senha definida anteriormente (por exemplo, "minhasenha")
# No prompt do PostgreSQL
CREATE DATABASE lojas;
\q

# Passo 3: Preenchendo o Banco de Dados
python FakeMigration.py

# Passo 4: Iniciando a API
python ReviewDb.py

# Passo 5: Adicionando um Usuário
python Auth.py register
# Siga as instruções fornecidas pelo programa para fornecer os detalhes do usuário a ser adicionado
