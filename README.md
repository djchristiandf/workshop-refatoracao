# Workshop sobre refatoração de API de leilões

Este projeto simula um serviço de leilão que já passou por refatoração e hoje deve ser mantido com boas práticas. O objetivo é deixar o código mais seguro, previsível e fácil de evoluir como um projeto pessoal, sem criar uma estrutura exagerada.

## O que foi melhorado

- API mais estável e com validações claras: cabeçalho obrigatório `X-Id-Usuario` e valor do lance validado como inteiro positivo.
- Tratamento de erros com respostas JSON consistentes para clientes HTTP.
- Endpoints expandidos:
  - `GET /leiloes` para listar todos os leilões.
  - `GET /leiloes/proximo` para acessar o próximo leilão agendado.
  - `GET /leiloes/<id>` para ver detalhes e lances de um leilão.
- Repositório separado: a camada de acesso a dados agora inclui busca de todos os leilões e próximo leilão.
- Projeto preparado para ambiente local com `.venv`, `requirements-dev.txt` e `.gitignore`.
- Dados iniciais passíveis de recriação via `schema.sql` e `seed.sql`.

## Estrutura de arquivos

- `app.py` - API Flask.
- `db.py` - conexão com PostgreSQL e gerenciamento de contexto Flask.
- `modelo/leilao.py` - regras de negócio do leilão.
- `repositorio/leilao.py` - consultas SQL.
- `test/` - suíte de testes com cobertura de regras de lance e rotas.
- `schema.sql` - script de criação de tabelas.
- `seed.sql` - script de dados iniciais.
- `.gitignore` - evita enviar ambiente local e arquivos temporários ao Git.

## Pré-requisitos

- Python 3.12+
- Docker (recomendado para PostgreSQL local)

## Configuração local

1. Ative o ambiente virtual:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

2. Instale dependências de runtime:

```sh
pip install -r requirements.txt
```

3. Instale dependências de desenvolvimento (teste):

```sh
pip install -r requirements-dev.txt
```

## Banco de dados com Docker

Suba o PostgreSQL local:

```sh
docker run --name workshop-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=banco1 \
  -p 5432:5432 \
  -d postgres:15
```

Crie o schema e os registros de exemplo:

```sh
docker exec -i workshop-postgres psql -U postgres -d banco1 < schema.sql
cat seed.sql | docker exec -i workshop-postgres psql -U postgres -d banco1
```

> Se você preferir, use `docker exec -i workshop-postgres psql -U postgres -d banco1` e cole o conteúdo de `schema.sql` e `seed.sql`.

## Executando a aplicação

No terminal com `.venv` ativado:

```sh
export DB_CONN_STRING="dbname=banco1 user=postgres password=postgres host=localhost"
export FLASK_APP=app.py
python -m flask run
```

## Testes

Execute a suíte com:

```sh
pytest test/ -v
```

Para gerar relatório de cobertura:

```sh
pytest --cov=app --cov=modelo --cov=repositorio --cov-report=term
```

## Uso básico da API

Listar leilões:

```sh
curl -s http://localhost:5000/leiloes
```

Ver detalhes de um leilão:

```sh
curl -s http://localhost:5000/leiloes/1
```

Ver o próximo leilão:

```sh
curl -s http://localhost:5000/leiloes/proximo
```

Registrar lance:

```sh
curl -i -X POST http://localhost:5000/leiloes/1/lances \
  -H "Content-Type: application/json" \
  -H "X-Id-Usuario: 43a72ab6-8abf-44c2-bf0b-4fdf9634bcd8" \
  -d '{"valor": 200}'
```

Lance mínimo:

```sh
curl -i -X POST http://localhost:5000/leiloes/1/lances/minimo \
  -H "X-Id-Usuario: 43a72ab6-8abf-44c2-bf0b-4fdf9634bcd8"
```

## Observações do refactor

A ideia foi manter este sistema como um projeto pessoal, simples e prático:
- arquitetura leve, com separação clara entre API, modelo e repositório;
- documentação do setup local, sem dependência de ferramentas complexas;
- testes automatizados que comprovam as regras de negócio importantes;
- `.gitignore` preparado para não versionar ambientes e arquivos temporários.

Poderá o projeto evoluir para incluir autenticação real, paginação de listagem e métricas DevOps mais tarde, mas a base agora está mais organizada para isso.
