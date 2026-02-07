import requests
import os
import pandas as pd


def download_data():
    """
    Baixa o arquivo Excel com todos os resultados da Mega Sena do site asloterias.com.br.
    Retorna o caminho do arquivo baixado ou None em caso de falha.
    """
    url = 'https://asloterias.com.br/download_excel.php'
    payload = {'l': 'ms', 't': 't', 'o': 's'}

    file_path = 'mega_sena_todos.xlsx'

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()

        with open(file_path, 'wb') as f:
            f.write(response.content)

        # Verifica se é um Excel válido
        try:
            pd.read_excel(file_path)
            return file_path
        except Exception as e:
            print(f'Erro ao validar arquivo Excel: {e}')
            if os.path.exists(file_path):
                os.remove(file_path)
            return None

    except requests.exceptions.RequestException as e:
        print(f'Erro no download: {e}')
        return None
