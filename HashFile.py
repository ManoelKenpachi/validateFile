import csv
import zipfile
import hashlib

def gerar_hashes_arquivo_zip(zip_file_path, csv_file_name):
    hashes = []

    # Abrir o arquivo zip
    with zipfile.ZipFile(zip_file_path, 'r') as arquivo_zip:
        # Extrair o arquivo CSV do arquivo zip
        arquivo_csv = arquivo_zip.extract(csv_file_name)

        # Ler os dados do arquivo CSV
        with open(arquivo_csv, 'r') as arquivo:
            leitor_csv = csv.reader(arquivo)
            dados = list(leitor_csv)

            # Ordenar as colunas
            # dados_ordenados = sorted(dados)

            # Gerar o hash para cada linha
            for linha in dados:
                linha_str = ','.join(linha)  # Converter a linha em uma string
                # print(linha_str)
                linha_hash = hashlib.md5(str(linha_str).encode()).hexdigest() # Gerar o hash SHA-256
                hashes.append(linha_hash)

    return hashes

# Exemplo de uso
zip_file_path = '/home/manoel/Napp/dados.zip'
csv_file_name = 'dados.csv'
resultado_hashes = gerar_hashes_arquivo_zip(zip_file_path, csv_file_name)

# Imprimir os hashes gerados
for i, hash in enumerate(resultado_hashes, start=1):
    if i == 1:
        continue
    print(f"Linha {i}: {hash}")
