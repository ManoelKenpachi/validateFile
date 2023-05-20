# Passo 1: Executando o Docker com PostgreSQL
```docker run --name postgres-db -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres```


# Passo 2: Preenchendo o Banco de Dados e gerando zip
```python FakeMigration.py ```

# Passo3: Criar um usuário
### ```python Auth.py ```
## ENDPOINT'S
- No insomnia importando o Insomnia.json, podera registrar um usuário no Banco de dados.
- Com o usuario gerar um token temporario de 30 minutos.
- Com o token temporário, um token que durará um dia.

# Passo 4: Iniciando validação
```python ReviewDb.py ```

Siga as instruções fornecidas pelo programa para fornecer os detalhes do usuário a ser adicionado
