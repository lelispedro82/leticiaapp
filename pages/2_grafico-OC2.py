import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Título da página
st.title("Análise: Crescimento dos Ativos vs. Resíduos - MQO")

# Carregando os dados
try:
    df = pd.read_excel("dados_r.xlsx")
except FileNotFoundError:
    st.error("Arquivo 'dados_r.xlsx' não encontrado no caminho 'leticiaapp/'.")
    st.stop()

# Filtros interativos
setores_disponiveis = df['setor'].dropna().unique()
anos_disponiveis = df['ano'].dropna().unique()

setor_dados = st.selectbox("Selecione o setor:", sorted(setores_disponiveis))
ano = st.selectbox("Selecione o ano:", sorted(anos_disponiveis, reverse=True))

# Selecionando os dados
dfmqo = df[(df['setor'] == setor_dados) & (df['ano'] == ano)]

# Verificação
if not dfmqo.empty:
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.regplot(x="creat", y="residuo", data=dfmqo,
                scatter_kws={"s": 50}, line_kws={"color": "red"}, ax=ax)

    for i in range(dfmqo.shape[0]):
        creat = dfmqo["creat"].iloc[i]
        residuo = dfmqo["residuo"].iloc[i]

        if np.isfinite(creat) and np.isfinite(residuo):
            ax.text(creat, residuo, dfmqo["ticker"].iloc[i], fontsize=9, ha='right')

    ax.set_title(f"Crescimento dos Ativos vs. Resíduos - Setor {setor_dados} ({ano}) - OC2")
    ax.set_xlabel("Crescimento dos Ativos")
    ax.set_ylabel("Resíduo da Regressão MQO")
    ax.grid(True)

    st.pyplot(fig)
else:
    st.warning(f"Não há dados disponíveis para o setor '{setor_dados}' no ano {ano}.")
