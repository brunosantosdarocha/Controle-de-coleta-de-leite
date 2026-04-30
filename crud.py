import streamlit as st
import sqlite3
import pandas as pd
from datetime import date 
import time

# 1. CONFIGURAÇÃO DA PÁGINA (Sempre a primeira coisa do Streamlit)
st.set_page_config(page_title="Sistema Laticínio", page_icon="🥛")

# 2. INICIALIZAÇÃO DO ESTADO DE ACESSO
# Usei session_state para controlar o acesso ao sistema, evitando que o usuário veja a tela de cadastro sem logar.
if 'acesso_liberado' not in st.session_state:
    st.session_state['acesso_liberado'] = False

# 3. LÓGICA DE NAVEGAÇÃO
# SE USUARIO E SENHA ESTIVEREM CORRETOS, ACESSO É LIBERADO E O SISTEMA DE CADASTRO É EXIBIDO
if st.session_state['acesso_liberado']:
    # ========================================================
    #SISTEMA DE CADASTRO E REGISTRO DE RECEBIMENTO DE LEITE
    # ========================================================
    
    # Todo CODIGO DO SISTEMA aqui dentro tem um recuo (TAB) para pertencer ao "if"
    
    conn = sqlite3.connect('leite.db', check_same_thread=False)
    cursor = conn.cursor()

    def criar_tabela():
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS leite2 (
                       id_recebimento INTEGER PRIMARY KEY AUTOINCREMENT,
                       nome_produtor TEXT,
                       data_recebimento DATE,
                       quantidade_leite INTEGER,
                       valor_leite FLOAT)
        """)
        conn.commit()

    def armazenar_produtor(nome_produtor):
        cursor.execute("INSERT INTO leite2 (nome_produtor) VALUES (?)", (nome_produtor,))
        conn.commit()
        st.toast(f"✅ Produtor '{nome_produtor}' cadastrado!", icon='👤')

    def armazenar_dados_recebimento(nome_produtor, data, quantidade, valor):
        cursor.execute("""
            INSERT INTO leite2 (nome_produtor, data_recebimento, quantidade_leite, valor_leite) 
            VALUES (?, ?, ?, ?)""", (nome_produtor, data, quantidade, valor))
        conn.commit()
        st.toast("✅ Dados salvos!", icon='🥛')

    def carregar_fornecedores():
        try:
            cursor.execute("SELECT DISTINCT nome_produtor FROM leite2 WHERE nome_produtor IS NOT NULL")
            nomes = [row[0] for row in cursor.fetchall()]
            return nomes if nomes else ["Nenhum produtor cadastrado"]
        except:
            return ["Erro ao carregar lista"]

    def carregar_dados_tabela():
        return pd.read_sql_query("SELECT * FROM leite2", conn)

    # Inicia o banco
    criar_tabela()

    # INTERFACE DO SISTEMA
    st.title("🚜 Sistema de Recebimento de Leite 🥛")
    
    if st.sidebar.button("Encerrar Sessão 🚪"):
        st.session_state['acesso_liberado'] = False
        st.rerun()

    # PARTE 1: CADASTRO
    st.subheader("🆕 1. Cadastrar Nome do Produtor")
    input_nome = st.text_input("Digite o nome completo do novo produtor")
    if st.button("Registrar Produtor"):
        if input_nome:
            armazenar_produtor(input_nome.upper())
            time.sleep(1)
            st.rerun()
        else:
            st.error("Digite um nome!")

    st.divider()

    # PARTE 2: REGISTRO DIÁRIO
    st.subheader("📝 2. Registrar Recebimento Diário")
    nome_sel = st.selectbox("SELECIONE O FORNECEDOR", carregar_fornecedores())
    data_rec = st.date_input("Data de recebimento", value=date.today(), format="DD/MM/YYYY")
    
    c1, c2 = st.columns(2)
    qtd = c1.number_input("Quantidade (Litros)", min_value=0)
    preco = c2.number_input("Preço (R$/L)", min_value=0.0, format="%.2f")

    if st.button("Registrar Recebimento"):
        if nome_sel != "Nenhum produtor cadastrado" and qtd > 0:
            armazenar_dados_recebimento(nome_sel, data_rec, qtd, preco)
            time.sleep(1)
            st.rerun()

    # PARTE 3: TABELA
    st.divider()

    st.subheader("📋 Painel Geral")
    df = carregar_dados_tabela()
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("Nenhum registro encontrado.")

else:
    # ========================================================
    # CÓDIGO (TELA DE LOGIN)
    # ========================================================
    
    st.title("🥛Gestão de Laticínios🧀")
    st.divider()
    
    with st.sidebar:
        st.header("Sobre o projeto")
        st.write("Sistema para controle de coleta e armazenamento de leite (Com tela de login).")

    with st.form("login_form"):
        st.subheader("Sistema de Login")
        user = st.text_input("Usuário")
        pw = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar", type="primary")

        if submit:
            if user == 'admin' and pw == 'admin123':
                st.toast("Login bem sucedido!", icon="✅")
                st.session_state['acesso_liberado'] = True
                time.sleep(1.5)
                st.rerun()
            else:
                st.toast("Usuário ou senha incorretos.", icon="❌")
