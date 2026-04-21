import streamlit as st
import pandas as pd
import os
import subprocess

# Configuração da página
st.set_page_config(page_title="Smart Job Hunter Dashboard", page_icon="🤖", layout="wide")

st.title("🤖 Smart Job Hunter Dashboard")

# Botão para rodar o bot
if st.sidebar.button("🚀 Rodar Busca Agora"):
    with st.spinner("Buscando novas vagas... Isso pode levar um minuto."):
        result = subprocess.run(["python3", "main.py"], capture_output=True, text=True)
        st.sidebar.success("Busca finalizada!")
        if result.stdout:
            st.sidebar.text_area("Log de Execução", result.stdout, height=100)

# Verificar se o arquivo existe
if not os.path.exists("jobs.csv"):
    st.error("O arquivo 'jobs.csv' ainda não foi gerado. Rode o bot primeiro!")
else:
    # Carregar dados
    try:
        df = pd.read_csv("jobs.csv")
        df['date'] = pd.to_datetime(df['date'])

        # Sidebar para Filtros
        st.sidebar.header("Filtros")
        search = st.sidebar.text_input("Buscar por cargo ou empresa")
        source_filter = st.sidebar.multiselect("Fonte", options=df['source'].unique(), default=df['source'].unique())

        # Filtro de Relevância (Palavras que VOCÊ quer)
        st.sidebar.subheader("🎯 Relevância")
        highlight_terms = st.sidebar.text_input("Termos para destacar (ex: Linux, Python)", "Linux, Python, Suporte")
        terms_list = [t.strip() for t in highlight_terms.split(",") if t.strip()]

        # Aplicar filtros
        mask = df['source'].isin(source_filter)
        if search:
            mask = mask & (df['title'].str.contains(search, case=False) | df['company'].str.contains(search, case=False))
        
        filtered_df = df[mask].sort_values(by='date', ascending=False)

        # Métricas no topo
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Acumulado", len(df))
        col2.metric("Vagas Filtradas", len(filtered_df))
        col3.metric("Novas Hoje", len(df[df['date'].dt.date == pd.Timestamp.now().date()]))
        col4.metric("Fontes", len(df['source'].unique()))

        st.divider()

        # Gráfico de Vagas por Dia
        st.subheader("📈 Evolução de Vagas")
        daily_counts = df.groupby(df['date'].dt.date).size().reset_index(name='vagas')
        st.line_chart(daily_counts.set_index('date'))

        # Exibição dos Dados
        st.subheader("📋 Lista de Oportunidades")
        
        def highlight_jobs(row):
            title = row['title'].lower()
            if any(term.lower() in title for term in terms_list):
                return ['background-color: #d4edda'] * len(row) # Verde claro para matches
            return [''] * len(row)

        # Formatação para exibição
        display_df = filtered_df.copy()
        display_df['link'] = display_df['link'].apply(lambda x: f'<a href="{x}" target="_blank">Abrir Vaga ↗️</a>')
        
        # Mostrar tabela formatada
        st.write(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")

st.sidebar.markdown("---")
st.sidebar.info("Bot configurado para LinkedIn, Indeed e Nerdin.")
