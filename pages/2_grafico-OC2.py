import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Evita warnings do Streamlit com matplotlib
import warnings
warnings.filterwarnings("ignore")

# Título do app
st.title("📈 Análise de Crescimento dos Ativos vs. Resíduos")
st.write("Gráfico de Crescimento dos Ativos em relação aos Resíduos da Regressão MQO por Setor e Ano")

# Carregar os dados do Excel diretamente
df = pd.read_excel("dados.xlsx")

# Interface para seleção de setor e ano
setores_disponiveis = df["setor"].dropna().unique()
anos_disponiveis = sorted(df["ano"].dropna().unique())

setor_dados = st.selectbox("Selecione o setor:", setores_disponiveis)
ano = st.selectbox("Selecione o ano:", anos_disponiveis)

# Filtrar os dados com base no setor e ano
dfmqo = df[(df["setor"] == setor_dados) & (df["ano"] == ano)]

if not dfmqo.empty:
    st.subheader(f"Gráfico: Setor de {setor_dados} - Ano {ano}")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.regplot(x="creat", y="residuo", data=dfmqo, scatter_kws={"s": 50}, line_kws={"color": "red"}, ax=ax)

    # Adicionar os rótulos com o ticker
    for i in range(dfmqo.shape[0]):
        creat = dfmqo["creat"].iloc[i]
        residuo = dfmqo["residuo"].iloc[i]

        if np.isfinite(creat) and np.isfinite(residuo):
            ax.text(creat, residuo, dfmqo["ticker"].iloc[i], fontsize=9, ha='right')

    ax.set_title(f"Crescimento dos Ativos vs. Resíduos - {setor_dados} ({ano}) - OC2")
    ax.set_xlabel("Crescimento dos Ativos")
    ax.set_ylabel("Resíduo da Regressão MQO")
    ax.grid(True)

    st.pyplot(fig)

else:
    st.warning(f"Não há dados disponíveis para o setor '{setor_dados}' no ano {ano}.")
