import psycopg2
from faker import Faker

import csv
import os
import zipfile


def verifica_cria_banco():
    # Configurações de conexão com o banco de dados
    db_host = "localhost"
    db_port = "5432"
    db_name = "postgres"
    db_user = "postgres"
    db_password = "mysecretpassword"

    # Estabelece a conexão com o banco de dados "postgres"
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )
    conn.autocommit = True

    # Cria o cursor para executar comandos SQL
    cur = conn.cursor()

    # Verifica se o banco de dados "Lojas" existe
    cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname='Lojas'")
    exists = cur.fetchone()

    if not exists:
        # Cria o banco de dados "Lojas" se não existir
        cur.execute("CREATE DATABASE Lojas")
        print("Banco de dados 'Lojas' criado com sucesso.")

    # Fecha o cursor e a conexão com o banco de dados
    cur.close()
    conn.close()


# Estabelece a conexão com o banco de dados
connection = psycopg2.connect(
    host='localhost',
    port=5432,
    database='Lojas',
    user='postgres',
    password='mysecretpassword'
)


def fakemigration():

    # Cria uma instância da classe Faker
    fake = Faker()

    # Define a quantidade de registros a serem inseridos
    num_records = 100

    # Cria um cursor para executar as operações SQL
    cursor = connection.cursor()

    create_table_query = '''
    CREATE TABLE dados (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255),
        phone VARCHAR(255),
        store_ref VARCHAR(255)

    );
    '''

    cursor.execute(create_table_query)
    connection.commit()

    create_user = '''
    CREATE TABLE users (
        username VARCHAR(255),
        password VARCHAR(255)

    );
    '''

    cursor.execute(create_user)
    connection.commit()

    # Confirma as alterações no banco de dados
    connection.commit()

    # Gera e insere os dados fictícios no banco de dados
    for _ in range(num_records):
        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()

        # Executa a operação SQL de inserção
        insert_query = f"INSERT INTO dados (name, email, phone, store_ref) VALUES ('{name}', '{email}', '{phone}', '1')"
        cursor.execute(insert_query)

    # Confirma as alterações no banco de dados
    connection.commit()

    # Gera e insere os dados fictícios no banco de dados
    for _ in range(num_records):
        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()

        # Executa a operação SQL de inserção
        insert_query = f"INSERT INTO dados (name, email, phone, store_ref) VALUES ('{name}', '{email}', '{phone}', '2')"
        cursor.execute(insert_query)

    # Confirma as alterações no banco de dados
    connection.commit()

    # Fecha o cursor e a conexão
    cursor.close()
    connection.close()

fakemigration()
