
def buscar(cur, id_leilao):
  cur.execute("""
    SELECT id, descricao, criador, data, diferenca_minima
    FROM leiloes
    WHERE id = %s
  """, (id_leilao, ))
  return cur.fetchone()


def buscar_todos(cur):
  cur.execute("""
    SELECT id, descricao, criador, data, diferenca_minima
    FROM leiloes
    ORDER BY data
  """)
  return cur.fetchall()


def buscar_proximo(cur):
  cur.execute("""
    SELECT id, descricao, criador, data, diferenca_minima
    FROM leiloes
    WHERE data >= now()
    ORDER BY data ASC
    LIMIT 1
  """)
  return cur.fetchone()


def buscar_lances(cur, id_leilao):
  cur.execute("""
    SELECT id, valor, comprador, data
    FROM lances
    WHERE id_leilao = %s
    ORDER BY data
  """, (id_leilao, ))
  return cur.fetchall()


def buscar_valor_ultimo_lance(cur, id_leilao):
  cur.execute("""
    SELECT valor
    FROM lances
    WHERE id_leilao = %s
    ORDER BY data DESC
    LIMIT 1
  """, (id_leilao, ))
  ultimo_lance = cur.fetchone()
  if ultimo_lance is None:
    return None
  return ultimo_lance[0]


def buscar_diferenca_minima(cur, id_leilao):
  cur.execute("""
    SELECT diferenca_minima
    FROM leiloes
    WHERE id = %s
  """, (id_leilao, ))
  leilao = cur.fetchone()
  if leilao is None:
    return None
  return leilao[0]


def inserir_lance(cur, id_leilao, valor, id_usuario):
  cur.execute("""
    INSERT INTO lances (id_leilao, valor, comprador, data)
    VALUES (%s, %s, %s, now())
  """, (id_leilao, valor, id_usuario))
