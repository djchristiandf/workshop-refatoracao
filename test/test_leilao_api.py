from test.fabricas.leilao import fabricar_leilao, fabricar_lance


def test_listar_leiloes(con, client):
  with con.cursor() as cur:
    fabricar_leilao(cur, id_=-1, descricao='Caneca Teste', diferenca_minima=50)
    fabricar_leilao(cur, id_=-2, descricao='Cadeira Teste', diferenca_minima=20)

  resp = client.get('/leiloes')
  assert resp.status_code == 200, 'A listagem de leilões deve responder com status 200.'
  json_resp = resp.json
  assert isinstance(json_resp, list)
  assert any(item['id'] == -1 for item in json_resp), 'O leilão -1 deve estar presente na lista.'
  assert any(item['id'] == -2 for item in json_resp), 'O leilão -2 deve estar presente na lista.'


def test_proximo_leilao(con, client):
  with con.cursor() as cur:
    fabricar_leilao(cur, id_=-1, descricao='Leilão Passado', data='2000-01-01 00:00', diferenca_minima=10)
    fabricar_leilao(cur, id_=-2, descricao='Próximo Leilão', data='2999-01-01 00:00', diferenca_minima=10)

  resp = client.get('/leiloes/proximo')
  assert resp.status_code == 200, 'O endpoint de próximo leilão deve responder 200 quando houver dados.'
  json_resp = resp.json
  assert json_resp['id'] == -2, 'O próximo leilão deve ser o de data mais próxima no futuro.'


def test_lance_sem_cabecalho_usuario(con, client):
  with con.cursor() as cur:
    fabricar_leilao(cur, id_=-1)

  resp = client.post('/leiloes/-1/lances', json={'valor': 100})
  assert resp.status_code == 400, 'A API deve recusar lances sem o cabeçalho X-Id-Usuario.'
  assert 'X-Id-Usuario' in resp.json['error'], 'A mensagem de erro deve informar o cabeçalho necessário.'
