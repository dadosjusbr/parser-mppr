import requests
import sys
import os 
import pathlib


URL_FORMATS = { 'membros-ativos-contracheque': 'http://apps.mppr.mp.br/planilhas_transparencia/mptransp{}{}mafp.ods',
                'membros-ativos-verbas-indenizatorias': 'http://apps.mppr.mp.br/planilhas_transparencia/mptransp{}{}mavio.ods'
        }
    
def download(url, file_path):
    try:
      response = requests.get(url, allow_redirects=True)
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
        download(url, file_path)
        
        files.append(file_path)
        
    return files
     