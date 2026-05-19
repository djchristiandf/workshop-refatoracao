from flask import Flask, jsonify, request
from http import HTTPStatus

import db
import repositorio.leilao
import modelo.leilao


app = Flask(__name__)


@app.teardown_appcontext
def liberar_conexao_gerenciada(_):
  db.liberar_conexao_gerenciada(testando=app.config.get('TESTING', False))


def erro_json(mensagem, status):
  return jsonify({'error': mensagem}), status


def extrair_usuario():
  usuario = request.headers.get('X-Id-Usuario')
  if not usuario:
    raise ValueError('Cabeçalho X-Id-Usuario é obrigatório.')
  return usuario


def validar_valor(dados):
  if not dados or 'valor' not in dados:
    raise ValueError('O corpo JSON deve conter o campo "valor".')
  try:
    valor = int(dados['valor'])
  except (TypeError, ValueError):
    raise ValueError('O campo "valor" deve ser um número inteiro.')
  if valor <= 0:
    raise ValueError('O valor do lance deve ser maior que zero.')
  return valor


def serializar_leilao(leilao, lances):
  return {
    'id': leilao[0],
    'descricao': leilao[1],
    'criador': leilao[2],
    'data': leilao[3].isoformat(),
    'diferenca_minima': leilao[4],
    'lances': [
      {
        'id': lance[0],
        'valor': lance[1],
        'comprador': lance[2],
        'data': lance[3].isoformat()
      }
      for lance in lances
    ]
  }


@app.route('/leiloes', methods=['GET'])
def listar_leiloes():
  with db.conexao_gerenciada().cursor() as cur:
    leiloes = repositorio.leilao.buscar_todos(cur)
    return jsonify([
      {
        'id': row[0],
        'descricao': row[1],
        'criador': row[2],
        'data': row[3].isoformat(),
        'diferenca_minima': row[4]
      }
      for row in leiloes
    ])


@app.route('/leiloes/proximo', methods=['GET'])
def get_proximo_leilao():
  with db.conexao_gerenciada().cursor() as cur:
    leilao = repositorio.leilao.buscar_proximo(cur)
    if leilao is None:
      return '', HTTPStatus.NO_CONTENT
    lances = repositorio.leilao.buscar_lances(cur, leilao[0])
    return jsonify(serializar_leilao(leilao, lances))


@app.route('/leiloes/<id_leilao>', methods=['GET'])
def get_detalhes_do_leilao(id_leilao):
  with db.conexao_gerenciada().cursor() as cur:
    leilao = repositorio.leilao.buscar(cur, id_leilao)
    if leilao is None:
      return erro_json('Leilão não encontrado.', HTTPStatus.NOT_FOUND)
    lances = repositorio.leilao.buscar_lances(cur, id_leilao)
    return jsonify(serializar_leilao(leilao, lances))


@app.route('/leiloes/<id_leilao>/lances', methods=['POST'])
def registrar_lance(id_leilao):
  try:
    dados = request.get_json(silent=True)
    valor = validar_valor(dados)
    id_usuario = extrair_usuario()
    with db.conexao_gerenciada().cursor() as cur:
      modelo.leilao.registrar_lance(cur, id_leilao, valor, id_usuario)
  except modelo.leilao.ValorMenorQueLanceAtual:
    return erro_json('Lance deve ser maior que o último.', HTTPStatus.BAD_REQUEST)
  except modelo.leilao.ValorMenorQueDiferencaMinima:
    return erro_json('Lance deve ser maior que o atual mais a diferença mínima.', HTTPStatus.BAD_REQUEST)
  except modelo.leilao.LanceDoCriador:
    return erro_json('Criador não pode dar lance.', HTTPStatus.BAD_REQUEST)
  except ValueError as err:
    return erro_json(str(err), HTTPStatus.BAD_REQUEST)
  return '', HTTPStatus.NO_CONTENT


@app.route('/leiloes/<id_leilao>/lances/minimo', methods=['POST'])
def registrar_lance_minimo(id_leilao):
  try:
    id_usuario = extrair_usuario()
    with db.conexao_gerenciada().cursor() as cur:
      valor_ultimo_lance = repositorio.leilao.buscar_valor_ultimo_lance(cur, id_leilao)
      diferenca_minima = repositorio.leilao.buscar_diferenca_minima(cur, id_leilao)
      valor = 1 if valor_ultimo_lance is None else valor_ultimo_lance + diferenca_minima
      modelo.leilao.registrar_lance(cur, id_leilao, valor, id_usuario)
  except modelo.leilao.LanceDoCriador:
    return erro_json('Criador não pode dar lance.', HTTPStatus.BAD_REQUEST)
  except ValueError as err:
    return erro_json(str(err), HTTPStatus.BAD_REQUEST)
  return '', HTTPStatus.NO_CONTENT
