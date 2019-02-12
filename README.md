# python_upload_spreadsheet
Projeto com exemplo de upload de planilha para cálculos

Aplicativo com funcionalidades para importação de dados com Python, Django e Pandas

## Pré-requisitos
* Python 3.6
* VirtualEnv / VirtualEnvWrapper
* Docker (Postgres)

## Características do projeto
O projeto é um aplicativo usando Django 2.1 e Pandas para cálculos em planilhas

## Preparando o projeto

Para executar o projeto é necessário criar uma virtualenv para isolar as dependências:
```
mkvirtualenv -p python3.6 python_upload_spreadsheet
workon python_upload_spreadsheet
```
Para instalar as dependências executar comando abaixo na raiz do projeto:
```
pip install -r requirements.txt
```

## Criar uma instância no Docker para Postgres
```
docker run --rm   --name postgres-docker -e POSTGRES_PASSWORD=postgres -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data  postgres
```
Para executar a imagem:
```
docker start postgres-docker
```

## Para executar o projeto
Depois de realizar os passos acima executar os seguintes comandos na raiz do projeto:
Para criar o banco com a tabela:
```
python manage.py migrate
```
Para executar os testes:
```
python manage.py test
```
Para executar o servidor http:
```
python manage.py runserver
```

## Para testar o corte de vídeo
Acessar o seguinte endereço:
```
http://localhost:8000/upload
```
Escolha uma planilha tab e realize o upload (Submit)
Ao final do processo será mostrado o resultado de todas as vendas realizadas.

## Serviços e urls disponíveis 

|Metodo|URL|Descrição|
|------|---|-----------|
|GET|/upload/|Exibe a interface de upload|
|POST|/upload/|Envia a planilha para um diretório e faz operações de cálculo|
