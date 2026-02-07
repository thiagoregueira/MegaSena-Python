# Análise de Dados da Mega Sena 🎲

Aplicação web desenvolvida em Python com Streamlit para análise estatística e visualização histórica dos resultados da Mega Sena. O projeto automatiza a coleta de dados, mantendo-se sempre atualizado com os últimos sorteios.

🔗 **Acesse online:** [https://amegasena.streamlit.app/](https://amegasena.streamlit.app/)

## ✨ Funcionalidades

- **Atualização Automática:**
  - Download automático de planilha com todos os resultados históricos.
  - Sincronização com API oficial da Caixa para sorteios do dia.
  - Botão de "Forçar Atualização" diretamente na interface.
- **Análise Estatística:**
  - Frequência de números sorteados por período.
  - Verificação de ocorrência de dezenas específicas.
  - Contagem de aparições conjuntas (par, terno, quadra, quina, sena).
- **Filtros Avançados:**
  - Filtragem por data ou número do concurso.
  - Interface interativa e responsiva.

## 🛠️ Tecnologias Utilizadas

- **[Python](https://www.python.org/)** - Linguagem principal.
- **[Streamlit](https://streamlit.io/)** - Framework para web app.
- **[Pandas](https://pandas.pydata.org/)** - Manipulação e análise de dados.
- **[SQLite](https://www.sqlite.org/index.html)** - Armazenamento local leve e eficiente.
- **Requests** - Consumo de APIs e download de arquivos.

## 📂 Estrutura do Projeto

```
/
├── data_manager.py      # Módulo responsável pelo download do Excel (Web Scraping/Request)
├── database_manager.py  # Gerenciamento do banco de dados SQLite e integração com API da Caixa
├── main.py              # Aplicação principal Streamlit e interface do usuário
├── styles.css           # Estilização personalizada da interface
├── requirements.txt     # Dependências do projeto
├── .gitignore           # Arquivos ignorados pelo Git
└── README.md            # Documentação do projeto
```

- **`data_manager.py`**: Realiza o download do arquivo `.xlsx` mais recente do site *As Loterias*.
- **`database_manager.py`**: Processa o Excel, alimenta o banco SQLite e verifica a API da Caixa para os dados mais recentes em tempo real.
- **`main.py`**: Orquestra a interface e interage com o usuário.

## 🚀 Como Executar Localmente

Siga os passos abaixo para rodar a aplicação em sua máquina:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/thiagoregueira/MegaSena-Python.git
   cd MegaSena-Python
   ```

2. **Crie um ambiente virtual (Opcional, mas recomendado):**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação:**
   ```bash
   streamlit run main.py
   ```

5. O navegador abrirá automaticamente em `http://localhost:8501`.

## 🔄 Fluxo de Atualização de Dados

O aplicativo possui um sistema inteligente de cache e atualização:
1. Ao iniciar, verifica se existe um banco de dados local.
2. Se não existir ou se o cache expirar (1 hora), tenta baixar a planilha atualizada.
3. Verifica a API da Caixa para garantir que até o sorteio de hoje (caso não esteja na planilha) seja incluído.
4. **Manual**: Você pode clicar no botão "🔄 Atualizar Dados" na barra lateral para forçar esse processo a qualquer momento.

## 📄 Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes (se aplicável).

---
Desenvolvido por **Thiago Regueira**. Dúvidas ou sugestões? Entre em contato!
