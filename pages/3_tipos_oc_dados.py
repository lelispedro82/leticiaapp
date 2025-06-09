import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Título
st.title("Empresas por Ano, Setor, Tipo de OC e Desempenho")

# Carregamento dos dados
try:
    df = pd.read_excel("dados_r.xlsx")
except FileNotFoundError:
    st.error("Arquivo 'dados_r.xlsx' não encontrado.")
    st.stop()

# Configurações
tipos_oc = ['oc1', 'oc2', 'oc3', 'oc4', 'oc41']
variaveis_desempenho = ['wroa', 'wroaebit', 'wroe', 'wqtobin', 'wmgop', 'wopor', 'lnat', 'divbrat']
setores_disponiveis = sorted(df['setor'].dropna().unique())

# Filtros interativos
setores_selecionados = st.multiselect("Selecione os setores:", setores_disponiveis)
tipos_oc_selecionados = st.multiselect("Selecione os tipos de OC:", tipos_oc)

# Validação
if not setores_selecionados or not tipos_oc_selecionados:
    st.warning("Selecione pelo menos um setor e um tipo de OC.")
    st.stop()

# Filtragem
df_filtrado = df[df['setor'].isin(setores_selecionados)]
filtro_oc = df_filtrado[tipos_oc_selecionados].sum(axis=1) >= 1
df_filtrado = df_filtrado[filtro_oc]

# Agrupamento por ano
contagem_por_ano = df_filtrado.groupby('ano').size().reset_index(name='quantidade')
contagem_por_ano = contagem_por_ano.sort_values('ano', ascending=False)

# Gráfico horizontal
if contagem_por_ano.empty:
    st.warning("Não há dados para os filtros selecionados.")
else:
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(contagem_por_ano['ano'].astype(str), contagem_por_ano['quantidade'], color='#1f77b4')

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                str(int(width)), va='center', fontsize=10)

    ax.set_xlabel("Quantidade de Empresas")
    ax.set_ylabel("Ano")
    ax.set_title(f"Empresas com OC = 1 ({', '.join(tipos_oc_selecionados)}) nos setores selecionados")
    ax.invert_yaxis()
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    # Tabela com detalhes das empresas
    colunas_exibir = ['ano', 'setor', 'ticker'] + tipos_oc_selecionados + variaveis_desempenho
    df_exibir = df_filtrado[colunas_exibir].copy()

    st.subheader("Dados das Empresas Selecionadas")
    st.dataframe(df_exibir, use_container_width=True)

    # Exportar para Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_exibir.to_excel(writer, index=False, sheet_name='Empresas')

    st.download_button(
        label="📥 Baixar dados em Excel",
        data=output.getvalue(),
        file_name="empresas_filtradas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
