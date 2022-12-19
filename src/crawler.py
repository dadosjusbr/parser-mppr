import requests
import sys
import os 
import pathlib


URL_FORMATS = { 'membros-ativos-contracheque': 'http://apps.mppr.mp.br/planilhas_transparencia/mptransp{}{}mafp.ods',
                'membros-ativos-verbas-indenizatorias': 'http://apps.mppr.mp.br/planilhas_transparencia/mptransp{}{}mavio.ods'
        }
    
def download(url, file_path, year, month):
    try:
      response = requests.get(url, allow_redirects=True)
    #   Quando o órgão não publica dados, o coletor baixa o html que retorna '404 Not Found'
      if response.status_code == 404:
          sys.stderr.write(f"Não existe planilhas para {month}/{year}.")
          sys.exit(4)
      with open(file_path, "wb") as file:
          file.write(response.content)
      file.close()
    except Exception as excep:
        sys.stderr.write("Não foi possível fazer o download do arquivo: " + file_path + '. O seguinte erro foi gerado: ' + excep )
        os._exit(1)


def crawl(year, month, output_path):
    files = []
    
    for key in URL_FORMATS:
        pathlib.Path(output_path).mkdir(exist_ok=True)
        filename = f'{key}-{month}-{year}.ods'
        file_path = f'{output_path}/{filename}'
        url = URL_FORMATS[key].format(year, month)
        download(url, file_path, year, month)
        
        files.append(file_path)
        
    return files
     