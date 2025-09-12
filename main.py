import sqlite3
from datetime import datetime  # noqa: F401

import openpyxl  # noqa: F401
import pandas as pd
import requests
import streamlit as st

# configurações da página
st.set_page_config(
    page_title='Análise de dados da Mega Sena',
    page_icon='🧊',
    layout='wide',
    initial_sidebar_state='expanded',
)

# importar o css
with open('styles.css') as f:  # noqa: PLW1514
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# lêr o arquivo excel mega_sena_asloterias_ate_concurso_2913_sorteio.xlsx
# df_excel = pd.read_excel('mega_sena_asloterias_ate_concurso_2913_sorteio.xlsx', skiprows=6)

# criar um banco de dados com os dados de df_excel
db = sqlite3.connect('mega_sena.db')
# cursor = db.cursor()
# cursor.execute(
#     'CREATE TABLE IF NOT EXISTS mega_sena (Concurso INTEGER PRIMARY KEY, Data TEXT, Bola1 INTEGER, Bola2 INTEGER, Bola3 INTEGER, Bola4 INTEGER, Bola5 INTEGER, Bola6 INTEGER)'
# )
# db.commit()

# inserir os dados de df_excel no banco de dados
# cursor.executemany(
#     'INSERT INTO mega_sena (Concurso, Data, Bola1, Bola2, Bola3, Bola4, Bola5, Bola6) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
#     df_excel.values,
# )
# db.commit()


# fazer uma requisição a api: https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena --
# para obter os dados mais recentes da mega sena
url = 'https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena'
response = requests.get(url)
data = response.json()


# se a resposta do data for 200, temos que pegar os seguintes dados: "numero", "dataApuracao", "dezenasSorteadasOrdemSorteio"
def get_api():
    if response.status_code == 200:
        concurso = int(data['numero'])
        # transformar a data em datetime
        data_sorteio = data['dataApuracao']
        # data_sorteio = datetime.strptime(data_sorteio, '%Y-%m-%dT%H:%M:%S.%fZ')
        # mapear cada bola sorteada para uma lista de inteiros
        bolas = data['dezenasSorteadasOrdemSorteio']
        bolas = list(map(int, bolas))
        return concurso, data_sorteio, bolas
    else:
        return 'Erro na requisição da API'


# criar função insert_data para inserir os dados da API no banco de dados se o numero do concurso não existir
def insert_data(db):
    concurso, data_sorteio, bolas = get_api()
    cursor = db.cursor()
    cursor.execute('SELECT Concurso FROM mega_sena WHERE Concurso = ?', (concurso,))
    if cursor.fetchone() is None:
        cursor.execute(
            'INSERT INTO mega_sena (Concurso, Data, Bola1, Bola2, Bola3, Bola4, Bola5, Bola6) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (
                concurso,
                data_sorteio,
                bolas[0],
                bolas[1],
                bolas[2],
                bolas[3],
                bolas[4],
                bolas[5],
            ),
        )
        db.commit()
    else:
        return 'Concurso já cadastrado'


# criar função get_data para recuperar a tabela "mega_sena" do banco de dados
def get_data(db):
    if insert_data(db) != 'Concurso já cadastrado':
        insert_data(db)
        df = pd.read_sql_query('SELECT * FROM mega_sena', db)
        return df
    else:
        df = pd.read_sql_query('SELECT * FROM mega_sena', db)
        return df


st.markdown(
    "<h1 style='text-align: center; color: #FFD700;'>Análise de dados da Mega Sena</h1>",
    unsafe_allow_html=True,
)
st.write('---')
st.write('#')
st.write('#')


# Pegar os DADOS
df = get_data(db)


# Transformar a coluna "Data" ques está no formato de data brasileiro em datetime
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')


# FILTROS
st.sidebar.title('Filtros')


# função filtro de data no sidebar
def filtro_data():
    data_inicio = st.sidebar.date_input('Data Inicial', df['Data'].min().date())
    data_fim = st.sidebar.date_input('Data Final', df['Data'].max().date())
    return pd.to_datetime(
        data_inicio,  # type: ignore
    ), pd.to_datetime(data_fim)  # type: ignore


# função filtro de concurso no sidebar
def filtro_concurso():
    concurso_inicio = st.sidebar.number_input('Concurso Inicial', min_value=1, max_value=df['Concurso'].max())
    concurso_fim = st.sidebar.number_input(
        'Concurso Final',
        min_value=concurso_inicio,
        max_value=df['Concurso'].max(),
        value=df['Concurso'].max(),
    )
    return concurso_inicio, concurso_fim


# definir o df com os filtros de datas
data_inicio, data_fim = filtro_data()
df_filtrado_datas = df[(df['Data'] >= data_inicio) & (df['Data'] <= data_fim)]

# criar um novo df contando quantas vezes cada bola foi sorteada, de acordo com o filtro de datas, criar um df com as colunas "Bola" e "Frequência"
# dropando as colunas que não usarei
df_filtrado_datas_frequencia_bolas = df_filtrado_datas.drop(columns=['Data', 'Concurso'])
# transformar o df em um formato de tabela
df_filtrado_datas_frequencia_bolas = df_filtrado_datas_frequencia_bolas.melt(var_name='Frequência', value_name='Bola')
# agrupar as bolas e contar quantas vezes cada uma foi sorteada
df_filtrado_datas_frequencia_bolas = df_filtrado_datas_frequencia_bolas.groupby('Bola').count()
# ordenar pela frequência
df_filtrado_datas_frequencia_bolas = df_filtrado_datas_frequencia_bolas.sort_values(by='Frequência', ascending=False)
# resetar o index
df_filtrado_datas_frequencia_bolas = df_filtrado_datas_frequencia_bolas.reset_index()


# criar colunas para exibir os df's lado a lado
col1, col2 = st.columns(2)

with col1:
    # mostrar o dataframe com os filtros de datas
    st.subheader('Dados filtrados por data:')
    st.dataframe(
        df_filtrado_datas.sort_values(by='Data', ascending=False),
        hide_index=True,
    )

with col2:
    # mostrar o dataframe com as frequências das bolas
    st.subheader('Frequência das bolas:')
    st.dataframe(df_filtrado_datas_frequencia_bolas, hide_index=True)


# definir o df com os filtros de concursos
concurso_inicio, concurso_fim = filtro_concurso()
df_filtrado_concursos = df[(df['Concurso'] >= concurso_inicio) & (df['Concurso'] <= concurso_fim)]

# criar um novo df contando quantas vezes cada bola foi sorteada, de acordo com o filtro de concursos, criar um df com as colunas "Bola" e "Frequência"
# dropando as colunas que não usarei
df_filtrado_concursos_frequencia_bolas = df_filtrado_concursos.drop(columns=['Data', 'Concurso'])
# transformar o df em um formato de tabela
df_filtrado_concursos_frequencia_bolas = df_filtrado_concursos_frequencia_bolas.melt(
    var_name='Frequência', value_name='Bola'
)
# agrupar as bolas e contar quantas vezes cada uma foi sorteada
df_filtrado_concursos_frequencia_bolas = df_filtrado_concursos_frequencia_bolas.groupby(
    'Bola'  # type: ignore
).count()
# ordenar pela frequência
df_filtrado_concursos_frequencia_bolas = df_filtrado_concursos_frequencia_bolas.sort_values(
    by='Frequência', ascending=False
)
# resetar o index
df_filtrado_concursos_frequencia_bolas = df_filtrado_concursos_frequencia_bolas.reset_index()


# criar colunas para exibir os df's lado a lado
col3, col4 = st.columns(2)

with col3:
    # mostrar o dataframe com os filtros de concursos
    st.subheader('Dados filtrados por número de concurso:')
    st.dataframe(
        df_filtrado_concursos.sort_values(by='Concurso', ascending=False),
        hide_index=True,
    )

with col4:
    # mostrar o dataframe com as frequências das bolas
    st.subheader('Frequência das bolas:')
    st.dataframe(df_filtrado_concursos_frequencia_bolas, hide_index=True)

st.write('#')
st.write('#')
st.write('#')

col5, col6, col7, col8, col9, col10 = st.columns(6)

with col5:
    number1 = st.number_input('Insira sua 1º dezena', min_value=1, max_value=60)
    # de acordo com a dezena escolhida informar quantas vezes ela foi sorteada
    st.write(
        f'A dezena {number1} foi sorteada {df_filtrado_datas_frequencia_bolas[df_filtrado_datas_frequencia_bolas["Bola"] == number1].iloc[0, 1]} vezes'
    )


with col6:
    number2 = st.number_input('Insira sua 2º dezena', min_value=1, max_value=60)
    # de acordo com a dezena escolhida informar quantas vezes ela foi sorteada
    st.write(
        f'A dezena {number2} foi sorteada {df_filtrado_datas_frequencia_bolas[df_filtrado_datas_frequencia_bolas["Bola"] == number2].iloc[0, 1]} vezes'
    )
    # informar também quantas vezes as duas dezenas foram sorteadas juntas
    st.write(
        f'As dezenas {number1} e {number2} foram sorteadas juntas {df_filtrado_datas[(df_filtrado_datas["Bola1"] == number1) & (df_filtrado_datas["Bola2"] == number2)].shape[0]} vezes'
    )

with col7:
    number3 = st.number_input('Insira sua 3º dezena', min_value=1, max_value=60)
    # de acordo com a dezena escolhida informar quantas vezes ela foi sorteada
    st.write(
        f'A dezena {number3} foi sorteada {df_filtrado_datas_frequencia_bolas[df_filtrado_datas_frequencia_bolas["Bola"] == number3].iloc[0, 1]} vezes'
    )
    # informar também quantas vezes as três dezenas foram sorteadas juntas
    st.write(
        f'As dezenas {number1}, {number2} e {number3} foram sorteadas juntas {df_filtrado_datas[(df_filtrado_datas["Bola1"] == number1) & (df_filtrado_datas["Bola2"] == number2) & (df_filtrado_datas["Bola3"] == number3)].shape[0]} vezes'
    )

with col8:
    number4 = st.number_input('Insira sua 4º dezena', min_value=1, max_value=60)
    # de acordo com a dezena escolhida informar quantas vezes ela foi sorteada
    st.write(
        f'A dezena {number4} foi sorteada {df_filtrado_datas_frequencia_bolas[df_filtrado_datas_frequencia_bolas["Bola"] == number4].iloc[0, 1]} vezes'
    )
    # informar também quantas vezes as quatro dezenas foram sorteadas juntas
    st.write(
        f'As dezenas {number1}, {number2}, {number3} e {number4} foram sorteadas juntas {df_filtrado_datas[(df_filtrado_datas["Bola1"] == number1) & (df_filtrado_datas["Bola2"] == number2) & (df_filtrado_datas["Bola3"] == number3) & (df_filtrado_datas["Bola4"] == number4)].shape[0]} vezes'
    )

with col9:
    number5 = st.number_input('Insira sua 5º dezena', min_value=1, max_value=60)
    # de acordo com a dezena escolhida informar quantas vezes ela foi sorteada
    st.write(
        f'A dezena {number5} foi sorteada {df_filtrado_datas_frequencia_bolas[df_filtrado_datas_frequencia_bolas["Bola"] == number5].iloc[0, 1]} vezes'
    )
    # informar também quantas vezes as cinco dezenas foram sorteadas juntas
    st.write(
        f'As dezenas {number1}, {number2}, {number3}, {number4} e {number5} foram sorteadas juntas {df_filtrado_datas[(df_filtrado_datas["Bola1"] == number1) & (df_filtrado_datas["Bola2"] == number2) & (df_filtrado_datas["Bola3"] == number3) & (df_filtrado_datas["Bola4"] == number4) & (df_filtrado_datas["Bola5"] == number5)].shape[0]} vezes'
    )

with col10:
    number6 = st.number_input('Insira sua 6º dezena', min_value=1, max_value=60)
    # de acordo com a dezena escolhida informar quantas vezes ela foi sorteada
    st.write(
        f'A dezena {number6} foi sorteada {df_filtrado_datas_frequencia_bolas[df_filtrado_datas_frequencia_bolas["Bola"] == number6].iloc[0, 1]} vezes'
    )
    # informar também quantas vezes as seis dezenas foram sorteadas juntas
    st.write(
        f'As dezenas {number1}, {number2}, {number3}, {number4}, {number5} e {number6} foram sorteadas juntas {df_filtrado_datas[(df_filtrado_datas["Bola1"] == number1) & (df_filtrado_datas["Bola2"] == number2) & (df_filtrado_datas["Bola3"] == number3) & (df_filtrado_datas["Bola4"] == number4) & (df_filtrado_datas["Bola5"] == number5) & (df_filtrado_datas["Bola6"] == number6)].shape[0]} vezes'
    )
