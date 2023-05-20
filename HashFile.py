import csv
import zipfile
import hashlib

def get_file_zip(zip_file_path, csv_file_name):
    hashes = []

    # Abrir o arquivo zip
    with zipfile.ZipFile(zip_file_path, 'r') as arquivo_zip:
        # Extrair o arquivo CSV do arquivo zip
        arquivo_csv = arquivo_zip.extract(csv_file_name)

        # Ler os dados do arquivo CSV
        with open(arquivo_csv, 'r') as arquivo:
            leitor_csv = csv.reader(arquivo)
            dados = list(leitor_csv)

            # Gerar o hash para cada linha
            for linha in dados:
                linha_str = ','.join(linha)  # Converter a linha em uma string
                linha_hash = hashlib.md5(str(linha_str).encode()).hexdigest() # Gerar o hash SHA-256
                hashes.append(linha_hash)

    return hashes