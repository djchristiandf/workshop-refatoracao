import logging
import os
import psycopg2
import psycopg2.extras
from flask import g


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def conexao_gerenciada():
  if 'conexao' not in g:
    g.conexao = abrir_conexao()
  return g.conexao


def liberar_conexao_gerenciada(testando=False):
  conexao = g.pop('conexao', None)
  if conexao is None:
    return

  if getattr(conexao, 'closed', 0):
    return

  conexao.commit()
  if not testando:
    conexao.close()


def abrir_conexao():
  db_conn_string = os.getenv('DB_CONN_STRING')
  if not db_conn_string:
    raise EnvironmentError('DB_CONN_STRING não está definido.')

  if os.getenv('DB_LOG_SQL', 'false').lower() in ('1', 'true', 'yes'):
    conexao = psycopg2.connect(
      db_conn_string,
      connection_factory=psycopg2.extras.LoggingConnection
    )
    conexao.initialize(logger)
  else:
    conexao = psycopg2.connect(db_conn_string)
  return conexao
