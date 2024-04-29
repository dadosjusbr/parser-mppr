import sys
import os

import pandas as pd

# Se for erro de não existir planilhas o retorno vai ser esse:
STATUS_DATA_UNAVAILABLE = 4
# Caso o erro for a planilha, que é invalida por algum motivo, o retorno vai ser esse:
STATUS_INVALID_FILE = 5


def _readOds(file):
    try:
        data = pd.read_excel(file, engine="odf").to_numpy()
    except Exception as excep:
        print(f"Erro lendo as planilhas: {excep}", file=sys.stderr)
        sys.exit(STATUS_INVALID_FILE)
    return data

def _readXls(file):
    try:
        data = pd.read_excel(file).to_numpy()
    except Exception as excep:
        print(f"Erro lendo as planilhas: {excep}", file=sys.stderr)
        sys.exit(STATUS_INVALID_FILE)
    return data


def load(file_names, year, month, output_path):
    """Carrega os arquivos passados como parâmetros.
    
     :param file_names: slice contendo os arquivos baixados pelo coletor.
    Os nomes dos arquivos devem seguir uma convenção e começar com 
    Membros ativos-contracheque e Membros ativos-Verbas Indenizatorias
     :param year e month: usados para fazer a validação na planilha de controle de dados
     :return um objeto Data() pronto para operar com os arquivos
    """

    contracheque = [c for c in file_names if "contracheque" in c][0]
    indenizatorias = [i for i in file_names if "indenizatorias" in i][0]
    
    if int(year) < 2023 or (int(year)==2023 and int(month) <= 5):
        contracheque = _readOds(contracheque)
        indenizatorias = _readOds(indenizatorias)
    else:
        contracheque = _readXls(contracheque)
        indenizatorias = _readXls(indenizatorias)

    return Data(contracheque, indenizatorias, year, month, output_path)

class Data:
    def __init__(self, contracheque, indenizatorias, year, month, output_path):
        self.year = year
        self.month = month
        self.output_path = output_path
        self.contracheque = contracheque
        self.indenizatorias = indenizatorias

    def validate(self):
        """
         Validação inicial dos arquivos passados como parâmetros.
        Aborta a execução do script em caso de erro.
         Caso o validade fique pare o script na leitura da planilha 
        de controle de dados dara um erro retornando o codigo de erro 4,
        esse codigo significa que não existe dados para a data pedida.
        """
        
        extension = "xls"
        if int(self.year) < 2023 or (int(self.year)==2023 and int(self.month) <= 5):
            extension = "ods"
            
        if not (
            os.path.isfile(
                f"{self.output_path}/membros-ativos-contracheque-{self.month}-{self.year}.{extension}"
            )
            or os.path.isfile(
                f"{self.output_path}/membros-verbas-indenizatorias-{self.month}-{self.year}.{extension}"
            )
        ):
            sys.stderr.write(f"Não existe planilhas para {self.month}/{self.year}.")
            sys.exit(STATUS_DATA_UNAVAILABLE)
