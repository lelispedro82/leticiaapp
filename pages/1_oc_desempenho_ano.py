import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("dados_r.xlsx")

st.title("📊 Excesso de Confiança e Desempenho financeiro por ano e por setor")
st.write("Este é o produto técnico com os dados da dissertação da Letícia 🎉")

# === Filtros no Sidebar ===
st.sidebar.header("🔎 Filtros Personalizados")

coluna_filtro = st.sidebar.selectbox("Escolha a variável de filtro:", ['oc1', 'oc2', 'oc3', 'oc4'])
opcoes = sorted(df[coluna_filtro].dropna().unique())
valores_selecionados = st.sidebar.multiselect(f"Valores de {coluna_filtro}:", opcoes, default=opcoes)

variavel_desempenho = st.sidebar.selectbox("Variável de desempenho:", ['wqtobin', 'wroa', 'wroaebit', 'wroe', 'wmgop'])
anos = st.sidebar.multiselect("Selecione os anos:", sorted(df['ano'].unique()), default=sorted(df['ano'].unique()))
setores = st.sidebar.multiselect("Selecione os setores:", sorted(df['setor'].unique()), default=sorted(df['setor'].unique()))

df_filtrado = df[
    (df[coluna_filtro].isin(valores_selecionados)) &
    (df['ano'].isin(anos)) &
    (df['setor'].isin(setores))
]

if variavel_desempenho in df_filtrado.columns:
    st.subheader(f"📉 Desempenho por Ano e Grupo de {coluna_filtro.upper()}")
    df_grouped = df_filtrado.groupby(['ano', coluna_filtro])[variavel_desempenho].mean().reset_index()

    fig3, ax3 = plt.subplots(figsize=(10, 6))
    for grupo in sorted(df_grouped[coluna_filtro].dropna().unique()):
        subset = df_grouped[df_grouped[coluna_filtro] == grupo]
        ax3.plot(subset['ano'], subset[variavel_desempenho], marker='o', label=f'Grupo {grupo}')

    ax3.set_title(f"{variavel_desempenho.upper()} Médio por Ano e {coluna_filtro.upper()}")
    ax3.set_xlabel("Ano")
    ax3.set_ylabel(f"{variavel_desempenho.upper()} Médio")
    ax3.set_xticks(sorted(df_grouped['ano'].unique()))
    ax3.grid(True)
    ax3.legend(title=coluna_filtro.upper())
    plt.tight_layout()
    st.pyplot(fig3)
else:
    st.warning(f"⚠️ A coluna '{variavel_desempenho}' não está disponível no DataFrame.")
