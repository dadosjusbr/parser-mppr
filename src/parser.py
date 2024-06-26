# coding: utf8
import sys
import os

from coleta import coleta_pb2 as Coleta

from headers_keys import (CONTRACHEQUE,
                          CONTRACHEQUE_2019,
                          INDENIZACOES_2019,
                          INDENIZACOES, HEADERS)
import number


def parse_employees(fn, chave_coleta, categoria):
    employees = {}
    counter = 1
    for row in fn:
        name = row[0]
        function = row[1]
        location = row[2]

        if "registros listados." in str(name) or "registro(s) listado(s)" in str(name):
            break
        if not number.is_nan(name) and name != "0" and name != "Nome" and "Unnamed" not in name :
            membro = Coleta.ContraCheque()
            membro.id_contra_cheque = chave_coleta + "/" + str(counter)
            membro.chave_coleta = chave_coleta
            membro.nome = name
            membro.funcao = function
            membro.local_trabalho = location
            membro.tipo = Coleta.ContraCheque.Tipo.Value("MEMBRO")
            membro.ativo = True
            
            membro.remuneracoes.CopyFrom(
                cria_remuneracao(row, categoria)
            )
          
            employees[name] = membro
            counter += 1
            
    return employees


def cria_remuneracao(row, categoria):
    remu_array = Coleta.Remuneracoes()
    items = list(HEADERS[categoria].items())
    for i in range(len(items)):
        key, value = items[i][0], items[i][1]
        remuneracao = Coleta.Remuneracao()
        remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneracao.categoria = categoria
        remuneracao.item = key
        # Caso o valor seja negativo, ele vai transformar em positivo:
        remuneracao.valor = float(abs(number.format_value(row[value])))

        if categoria == CONTRACHEQUE and value in [13, 14, 15]:
            remuneracao.valor = remuneracao.valor * (-1)
            remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("D")
        elif categoria == CONTRACHEQUE_2019 and value in [12, 13, 14]:
            remuneracao.valor = remuneracao.valor * (-1)
            remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("D")
        else: 
            remuneracao.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")

        if (
            categoria == CONTRACHEQUE or categoria == CONTRACHEQUE_2019
           ) and value in [4]:
            remuneracao.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("B")

        remu_array.remuneracao.append(remuneracao)

    return remu_array


def update_employees(fn, employees, categoria):
    for row in fn:
        nome = row[0]
        if nome in employees.keys():
            emp = employees[nome]
            remu = cria_remuneracao(row, categoria)
            emp.remuneracoes.MergeFrom(remu)
            employees[nome] = emp
    return employees


def parse(data, chave_coleta, month, year):
    employees = {}
    folha = Coleta.FolhaDePagamento()

    # Puts all parsed employees in the big map
    if year == "2018" or year == "2019":
        employees.update(parse_employees(data.contracheque, chave_coleta, CONTRACHEQUE_2019))
    else:
        employees.update(parse_employees(data.contracheque, chave_coleta, CONTRACHEQUE))

    if year == "2018" or (year == "2019" and int(month) < 10):
        update_employees(data.indenizatorias, employees, INDENIZACOES_2019)
    else:
        update_employees(data.indenizatorias, employees, INDENIZACOES)

    for i in employees.values():
        folha.contra_cheque.append(i)
    return folha
