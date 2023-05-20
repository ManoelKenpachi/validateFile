import psycopg2
from faker import Faker

import csv
import os
import zipfile

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

def export_data_to_csv_and_zip():
    # Nome do arquivo CSV e ZIP
    csv_filename = 'dados.csv'
    zip_filename = 'dados.zip'
    
    try:
        cursor = connection.cursor()
        
        # Executa a consulta SELECT
        cursor.execute('SELECT id, name FROM dados')
        rows = cursor.fetchall()
        
        # Verifica se existem resultados
        if not rows:
            print('Nenhum dado encontrado.')
            return
        
        # Gera o arquivo CSV
        with open(csv_filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([desc[0] for desc in cursor.description])  # Escreve os cabeçalhos das colunas
            csv_writer.writerows(rows)  # Escreve os dados
        
        # Cria o arquivo ZIP
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            zipf.write(csv_filename, os.path.basename(csv_filename))
        
        print('Arquivo ZIP criado com sucesso.')
        
    except psycopg2.Error as e:
        print('Ocorreu um erro ao exportar os dados:', str(e))
        
    finally:
        # Fecha o cursor e a conexão
        cursor.close()
        connection.close()
        
        # Remove o arquivo CSV
        if os.path.exists(csv_filename):
            os.remove(csv_filename)

export_data_to_csv_and_zip()