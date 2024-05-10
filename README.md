# Análise de dados da Mega Sena

Este projeto é uma análise de dados da Mega Sena, utilizando Python, Streamlit, Pandas, SQLite e uma API da Caixa Econômica Federal.

## Estrutura do Projeto

```
.gitignore
main.py
mega_sena.db
requirements.txt
styles.css
```

## Descrição dos Arquivos

- \[``main.py``\]: Este é o arquivo principal do projeto. Ele configura a página do Streamlit, lê os dados do arquivo Excel, cria um banco de dados SQLite, insere os dados do Excel no banco de dados e faz uma requisição à API da Caixa para obter os dados mais recentes da Mega Sena.

- \[``requirements.txt``\]: Este arquivo lista todas as dependências do projeto.

- \[``styles.css``\]: Este arquivo contém os estilos CSS usados na página do Streamlit.

- \[``.gitignore``\]: Este arquivo lista todos os arquivos e diretórios que o Git deve ignorar.

- \[``mega_sena.db``\]: Dados de todos os concursos da megasena.



## Como Executar o Projeto

1. Clone o repositório.

2. Instale as dependências listadas no arquivo \[``requirements.txt``\] usando o comando `pip install -r requirements.txt`.

3. Execute o arquivo \[``main.py``\] usando o comando `streamlit run main.py`.

4. O projeto também está em produção através do endereço: [https://amegasena.streamlit.app/](https://amegasena.streamlit.app/)

## Dependências

- Streamlit
- Pandas
- openpyxl
- requests
- sqlite3

## Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## Contato

Se você tiver alguma dúvida ou sugestão, sinta-se à vontade para entrar em contato.
