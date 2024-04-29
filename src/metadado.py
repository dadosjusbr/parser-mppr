from coleta import coleta_pb2 as Coleta


def captura(month, year):
    metadado = Coleta.Metadados()
    metadado.estritamente_tabular = False
    metadado.tem_matricula = False
    metadado.tem_lotacao = True
    metadado.tem_cargo = True
    metadado.receita_base = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    metadado.despesas = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    metadado.formato_consistente = True
    metadado.outras_receitas = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    """
    Nessa data ocorre uma mudança nos formatos das planilhas,
    tanto as de remunerações quando as indenizatorias.
    """
    if (year == 2019 and month == 10) or (year == 2020 and month == 1):
        metadado.formato_consistente = False
        
    if year < 2023 or (year == 2023 and month <= 5):
        metadado.acesso = Coleta.Metadados.FormaDeAcesso.ACESSO_DIRETO
        metadado.extensao = Coleta.Metadados.Extensao.ODS
    else:
        metadado.acesso = Coleta.Metadados.FormaDeAcesso.NECESSITA_SIMULACAO_USUARIO
        metadado.extensao = Coleta.Metadados.Extensao.XLS

    return metadado
