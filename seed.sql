INSERT INTO leiloes (descricao, criador, data, diferenca_minima)
VALUES ('Caneca', 'efd28c1e-2538-4842-a97a-92759903c2fa', now(), 500);

INSERT INTO leiloes (descricao, criador, data, diferenca_minima)
VALUES ('Cadeira', 'efd28c1e-2538-4842-a97a-92759903c2fa', now(), 1);

INSERT INTO lances (valor, comprador, data, id_leilao)
VALUES (501, '1027c0fc-77c8-44d0-8b0b-4fdf9634bcd8', now(), 1);

INSERT INTO lances (valor, comprador, data, id_leilao)
VALUES (1001, '05feb8af-89a1-4320-bf0f-29dc1b8754c5', now(), 1);
