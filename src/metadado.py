from coleta import coleta_pb2 as Coleta


def captura(month, year):
    metadado = Coleta.Metadados()
    metadado.acesso = Coleta.Metadados.FormaDeAcesso.ACESSO_DIRETO
    metadado.extensao = Coleta.Metadados.Extensao.ODS
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
    if (year == 2020 and month == 1):
        metadado.formato_consistente = False
        
    return metadado
