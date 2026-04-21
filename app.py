import streamlit as st
import pandas as pd
import os

# Configuração da página
st.set_page_config(page_title="Smart Job Hunter Dashboard", page_icon="🤖", layout="wide")

st.title("🤖 Smart Job Hunter Dashboard")
st.markdown("Acompanhe em tempo real as vagas rastreadas pelo bot.")

# Verificar se o arquivo existe
if not os.path.exists("jobs.csv"):
    st.error("O arquivo 'jobs.csv' ainda não foi gerado. Rode o bot primeiro!")
else:
    # Carregar dados
    df = pd.DataFrame()
    try:
        df = pd.read_csv("jobs.csv")
        # Garantir que links sejam clicáveis
        def make_clickable(link):
            return f'<a href="{link}" target="_blank">Ver Vaga</a>'
        
        # Sidebar para Filtros
        st.sidebar.header("Filtros")
        search = st.sidebar.text_input("Buscar por cargo ou empresa")
        source_filter = st.sidebar.multiselect("Fonte", options=df['source'].unique(), default=df['source'].unique())

        # Aplicar filtros
        filtered_df = df[df['source'].isin(source_filter)]
        if search:
            filtered_df = filtered_df[
                filtered_df['title'].str.contains(search, case=False) | 
                filtered_df['company'].str.contains(search, case=False)
            ]

        # Métricas no topo
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Vagas", len(df))
        col2.metric("Vagas Filtradas", len(filtered_df))
        col3.metric("Fontes Ativas", len(df['source'].unique()))

        st.divider()

        # Exibição dos Dados
        st.subheader("📋 Vagas Encontradas")
        
        # Criar uma cópia para exibição com links clicáveis
        display_df = filtered_df.copy()
        display_df['link'] = display_df['link'].apply(make_clickable)
        
        # Mostrar tabela usando HTML para renderizar os links
        st.write(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")

st.sidebar.markdown("---")
st.sidebar.info("Desenvolvido para fins de estudo e automação de carreira.")
