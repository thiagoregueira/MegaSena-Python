import sqlite3
import pandas as pd
import os
import requests
from data_manager import download_data
import streamlit as st

DB_NAME = 'mega_sena.db'


def get_api_latest():
    """Busca o último sorteio da API da Caixa (ServiceBus)"""
    url = 'https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena'
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            concurso = int(data['numero'])
            data_sorteio = data['dataApuracao']
            # A API retorna strings, converte para int
            bolas = list(map(int, data['dezenasSorteadasOrdemSorteio']))
            return concurso, data_sorteio, bolas
    except Exception as e:
        print(f'Erro ao acessar API da Caixa: {e}')
    return None


def init_db():
    """Cria a tabela se não existir."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS mega_sena (Concurso INTEGER PRIMARY KEY, Data TEXT, Bola1 INTEGER, Bola2 INTEGER, Bola3 INTEGER, Bola4 INTEGER, Bola5 INTEGER, Bola6 INTEGER)'
    )
    conn.commit()
    conn.close()


def update_from_excel():
    """Baixa o Excel e atualiza o banco de dados."""
    excel_file = download_data()
    if not excel_file:
        return False

    try:
        # Lê o Excel pulando as 6 primeiras linhas de cabeçalho inútil
        df = pd.read_excel(excel_file, skiprows=6)

        # Seleciona apenas as colunas relevantes e renomeia para garantir
        # Assume que a ordem é: Concurso, Data, Bola1..6
        df = df.iloc[:, 0:8]
        df.columns = ['Concurso', 'Data', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Limpa dados antigos para garantir consistência total com o arquivo oficial
        cursor.execute('DELETE FROM mega_sena')

        # Insere dados em lote
        cursor.executemany(
            'INSERT INTO mega_sena (Concurso, Data, Bola1, Bola2, Bola3, Bola4, Bola5, Bola6) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            df.values.tolist(),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f'Erro ao processar Excel: {e}')
        return False


def check_api_update():
    """Verifica se há um sorteio mais novo na API da Caixa e insere."""
    latest = get_api_latest()
    if latest:
        concurso, data_sorteio, bolas = latest
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute('SELECT Concurso FROM mega_sena WHERE Concurso = ?', (concurso,))
        if cursor.fetchone() is None:
            cursor.execute(
                'INSERT INTO mega_sena (Concurso, Data, Bola1, Bola2, Bola3, Bola4, Bola5, Bola6) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (concurso, data_sorteio, *bolas),
            )
            conn.commit()
            print(f'Sorteio {concurso} inserido via API.')
        conn.close()


@st.cache_data(ttl=3600)
def load_data(force_update=False):
    """
    Função principal para ser usada no Streamlit.
    Carrega os dados, atualizando se necessário (cache expira em 1h).
    force_update: Se True, força o download e atualização.
    """
    init_db()

    # Se o banco não existe ou for forçado, tenta atualizar do Excel
    if force_update or not os.path.exists(DB_NAME):
        update_from_excel()

    # Sempre tenta pegar o último da API para garantir tempo real
    check_api_update()

    conn = sqlite3.connect(DB_NAME)
    try:
        df = pd.read_sql_query('SELECT * FROM mega_sena', conn)
    except Exception:
        return pd.DataFrame()
    finally:
        conn.close()

    return df
