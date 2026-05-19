DROP TABLE IF EXISTS lances;
DROP TABLE IF EXISTS leiloes;

CREATE TABLE leiloes (
  id serial PRIMARY KEY,
  descricao text NOT NULL,
  criador uuid NOT NULL,
  data timestamp with time zone NOT NULL,
  diferenca_minima smallint NOT NULL
);

CREATE TABLE lances (
  id serial PRIMARY KEY,
  valor smallint NOT NULL,
  comprador uuid NOT NULL,
  data timestamp with time zone NOT NULL,
  id_leilao int NOT NULL,
  CONSTRAINT fk_lances_leilao FOREIGN KEY (id_leilao) REFERENCES leiloes (id)
);
