🥛 Sistema de Gestão: Coleta e Armazenamento de Leite
VERSAO 1.2
Este projeto é uma aplicação End-to-End desenvolvida para otimizar o controle operacional em laticínios. Ele resolve o problema de registros manuais, transformando a coleta diária de leite em um banco de dados estruturado com interface interativa.

🚀 Funcionalidades Principais
Autenticação de Segurança: Tela de login com controle de estado (Session State), garantindo que apenas usuários autorizados acessem os registros.

Gestão de Fornecedores: Módulo para cadastro de novos produtores com padronização de dados.

Registro de Recebimento: Lançamento diário de litragem e preços, com cálculos automáticos de valores totais.

Painel de Dados (Analytics): Visualização dinâmica de tabelas utilizando Pandas, com filtros automáticos e formatação de moeda brasileira (R$).

Persistência de Dados: Integração total com banco de dados SQLite para armazenamento seguro e confiável.

🛠️ Tecnologias Utilizadas
Linguagem: Python 3.x

Interface Web: Streamlit

Banco de Dados: SQLite3

Manipulação de Dados: Pandas

Estilização: CSS Customizado e Emojis Nativos

📊 Estrutura do Banco de Dados (SQL)
A tabela leite2 foi projetada para garantir a integridade referencial e facilidade na extração de relatórios:

SQL
CREATE TABLE IF NOT EXISTS leite2 (
    id_recebimento INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_produtor TEXT NOT NULL,
    data_recebimento DATE,
    quantidade_leite INTEGER,
    valor_leite FLOAT
);
📦 Como Executar o Projeto
Clone o repositório:

Bash
git clone [https://github.com/brunosantosdarocha/Controle-de-coleta-de-leite).git]
Instale as dependências:

Bash
pip install streamlit pandas
Execute a aplicação:

Bash
streamlit run seu_arquivo.py
💡 Motivação e Contexto
Este sistema nasceu da necessidade prática de substituir planilhas físicas e controles informais por uma solução digital robusta. Durante o desenvolvimento, apliquei conceitos de Lógica de Programação, Modelagem de Dados e UX (User Experience) para criar uma ferramenta que fosse útil tanto para o operador de campo quanto para o gestor financeiro.

👤 Autor
Bruno – Administrativo / IT Professional / Desenvolvedor em Formação

LinkedIn: [https://www.linkedin.com/in/bruno-rocha-82a85b345]

Objetivo: Transição para Análise de Dados e Desenvolvimento.
