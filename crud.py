
import streamlit as st
import sqlite3
import pandas as pd
from datetime import date # Importação necessária para definir a data padrão

# CONFIGURAÇÕES DO BANCO DE DADOS 
# check_same_thread=False é crucial para o Streamlit não dar erro de thread
conn = sqlite3.connect('leite.db', check_same_thread=False)
cursor = conn.cursor()

# DEFINIÇÃO DAS FUNÇÕES (Lógica) 

def criar_tabela():
    #Cria a tabela no banco de dados, caso ela ainda não exista.
    # MODIFICAÇÃO: Executei o commit dentro da função para garantir a criação física
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leite2 (
                   id_recebimento INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome_produtor TEXT,
                   data_recebimento DATE,
                   quantidade_leite INTEGER,
                   valor_leite FLOAT)
    """)
    conn.commit()

     
    #Função para armazenar APENAS um novo produtor.

def armazenar_produtor(nome_produtor):
   
    cursor.execute("INSERT INTO leite2 (nome_produtor) VALUES (?)", (nome_produtor,))
    conn.commit()

    st.toast(f"✅ Produtor '{nome_produtor}' cadastrado com sucesso!", icon='👤')

#Função para armazenar os DEMAIS DADOS vinculados ao produtor.
def armazenar_dados_recebimento(nome_produtor, data, quantidade, valor):
   
    # O SQL usa ? como espaços reservado para os valores
    cursor.execute("""
        INSERT INTO leite2 (nome_produtor, data_recebimento, quantidade_leite, valor_leite) 
        VALUES (?, ?, ?, ?)""", (nome_produtor, data, quantidade, valor))
    conn.commit()
    st.toast("✅ Dados de recebimento armazenados!", icon='🥛')

def carregar_fornecedores():
    #Busca nomes únicos já cadastrados no banco para o selectbox.
    try:
        # Buscamos nomes únicos onde já houve cadastro de produtor
        cursor.execute("SELECT DISTINCT nome_produtor FROM leite2 WHERE nome_produtor IS NOT NULL")
        # row[0] extrai a string de dentro da tupla retornada pelo SQLite
        nomes = [row[0] for row in cursor.fetchall()]
        
        # Se o banco estiver vazio, retorna uma lista padrão limpa
        return nomes if nomes else ["Nenhum produtor cadastrado"]
    except:
        # Fallback de segurança
        return ["Erro ao carregar lista"]
    
    #Carrega todos os registros para exibir no dataframe.
def carregar_dados_tabela():
    query = "SELECT * FROM leite2"
    return pd.read_sql_query(query, conn)


# INICIALIZAÇÃO DO PROGRAMA
# Cria a tabela se ela não existir ao rodar o script
criar_tabela()


#  INTERFACE GRÁFICA

st.title(" Sistema de Recebimento de Leite🥛") # Título



# PRIMEIRA PARTE : CADASTRO DO NOME DO PRODUTOR

st.subheader("🆕 1. Cadastrar Nome do Produtor")

# CAMPO PARA INSERIR O NOME DO PRODUTOR
input_nome_produtor = st.text_input("Digite o nome completo do novo produtor", max_chars=50)

# Botão de submit DA PARTE 1 (Cadastro do produtor)
btn_cadastrar_produtor = st.button("Registrar Produtor")

# Lógica exclusiva DA PARTE  1
if btn_cadastrar_produtor:
    st.write(f"Registrando produtor: {input_nome_produtor}")
    # Verifica se o campo não está vazio antes de tentar salvar
    if input_nome_produtor:
        armazenar_produtor(input_nome_produtor.upper()) # .UPPER() para padronizar os nomes em maiúsculas
        st.rerun()         #st.rerun() é necessário para atualizar o selectbox do bloco 2 instantaneamente

    else:
        st.error("⚠️ Por favor, digite o nome do produtor.")


st.divider() # LINHA PARA DIVIDIROS BLOCOS


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# PARTE 2: REGISTRO DOS DEMAIS DADOS
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>^
st.subheader("📝 2. Registrar Recebimento de Leite Diário")

# Selectbox que carrega os nomes já cadastrados no BLOCO 1
input_selectbox_nome = st.selectbox("SELECIONE O FORNECEDOR", carregar_fornecedores())

# Data Input (MODIFICAÇÃO: definimos date.today() como valor padrão brasileiro)
input_data = st.date_input("Data de recebimento", format="DD/MM/YYYY", value=date.today())

# Colunas para organizar Litros e Preço lado a lado
col1, col2 = st.columns(2)
with col1:
    input_quantidade_leite = st.number_input("Quantidade de leite (Litros)", min_value=0, step=1)
with col2:
    input_valor_leite = st.number_input("Preço do leite (R$ por Litro)", min_value=0.0, format="%.2f", step=0.05)

# Cálculo automático (MODIFICAÇÃO: movido para fora do bloco IF para estar sempre disponível)
total_dia = input_quantidade_leite * input_valor_leite

# Botão de submit do BLOCO 2 (Independente)
btn_registrar_leite = st.button("Registrar recebimento de leite")

# Lógica exclusiva do BLOCO 2
if btn_registrar_leite:
    # Verificações básicas antes de salvar
    if input_selectbox_nome != "Nenhum produtor cadastrado" and input_quantidade_leite > 0 and input_valor_leite > 0:
        # Feedback visual antes de salvar
        st.write(f"Resumo: {input_selectbox_nome} || {input_quantidade_leite}L || Total R$ {total_dia:.2f}")
        
        # Chama a função SQL (Passo 4.2 do tutorial anterior)
        # O nome selecionado no selectbox é vinculado ao novo registro
        armazenar_dados_recebimento(input_selectbox_nome, input_data, input_quantidade_leite, input_valor_leite)
        st.rerun() # Atualiza a tabela abaixo instantaneamente
    else:
        st.error("⚠️ Verifique se selecionou um produtor e se Qtd/Preço são maiores que zero.")

st.divider() # Linha divisória antes da tabela


# ============================================================
# VISUALIZAÇÃO DOS DADOS
# ============================================================
st.subheader("📋 Painel Geral de Recebimento")

# 1. Carrega os dados mais recentes do banco
df = carregar_dados_tabela()

# 2. Configura a exibição da tabela (Mantivemos a formatação solicitada anteriormente)
if not df.empty:
    st.dataframe(
        df,
        use_container_width=True, # Ocupa toda a largura da tela
        hide_index=True,           # Esconde a coluna de números (índice) do Pandas
        
        # column_config permite configurar cada coluna individualmente
        column_config={
            # 1. Esconde a coluna ID (o usuário comum não precisa ver)
            "id_recebimento": None, 
            
            # 2. Formata o Nome do Produtor
            "nome_produtor": st.column_config.TextColumn(
                "👨‍🌾 Nome do Produtor",
                width="medium"
            ),
            
            # 3. Formata a Data (DD/MM/YYYY)
            "data_recebimento": st.column_config.DateColumn(
                "📅 Data de Entrega",
                format="DD/MM/YYYY", # Formato brasileiro
                width="small"
            ),
            
            # 4. Formata a Quantidade (Números Inteiros)
            "quantidade_leite": st.column_config.NumberColumn(
                "🥛 Litros (L)",
                format="%d L", # %d para inteiro, adiciona " L" no final
                width="small"
            ),
            
            # 5. Formata o Valor (Moeda R$)
            "valor_leite": st.column_config.NumberColumn(
                "💰 Preço (R$/L)",
                format="R$ %.2f", # R$ seguido de número com 2 casas decimais
                width="small"
            )
        }
    )
    
    # --- TOTAL GERAL ---
    st.write("---") # Linha fina
    total_litros = df['quantidade_leite'].sum()
    st.info(f"**Total acumulado de leite recebido:** {total_litros} Litros.")

else:
    st.warning("⚠️ Nenhum registro de recebimento encontrado.")