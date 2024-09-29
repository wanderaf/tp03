import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Função para carregar os dados e utilizar cache
@st.cache_data
def load_data(uploaded_file, separator):
    return pd.read_csv(uploaded_file, sep=separator)

# Configuração inicial do Session State
if "background_color" not in st.session_state:
    st.session_state["background_color"] = "#FFFFFF"
if "text_color" not in st.session_state:
    st.session_state["text_color"] = "#000000"
if "filtered_data" not in st.session_state:
    st.session_state["filtered_data"] = None

# Barra lateral para as configurações de personalização de cor
st.sidebar.header("Personalize o Layout")
background_color = st.sidebar.color_picker("Escolha a cor de fundo:", st.session_state["background_color"])
text_color = st.sidebar.color_picker("Escolha a cor da fonte:", st.session_state["text_color"])

# Aplica as preferências de cor na interface usando CSS via markdown
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {background_color};
        color: {text_color};
    }}
    h1, h2, h3, h4, h5, h6, p, div {{
        color: {text_color} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# Seção de "Explicação e Motivação" usando markdown para títulos
st.markdown(f"<h1 style='color: {text_color};'>Explicação e Motivação</h1>", unsafe_allow_html=True)

# Carrega e exibe a imagem do Rio de Janeiro
st.image(r'img/rioDeJaneiro.jpg', caption="Rio de Janeiro", use_column_width=True)

# Explicação do objetivo e motivação
st.markdown(f"""
<div style="color: {text_color};">
    <b>Objetivo do Dashboard</b>: O objetivo deste painel é fornecer uma visão geral e interativa sobre os dados de turismo do Rio de Janeiro. Através de gráficos, tabelas e métricas interativas, gestores públicos, pesquisadores e turistas podem acessar informações atualizadas sobre o impacto do turismo na cidade.
    </br></br>
    <b>Motivação</b>: O turismo é um dos setores mais importantes para a economia do Rio de Janeiro. Ao criar um dashboard acessível e visualmente atraente, buscamos simplificar a análise dos dados, identificar tendências e facilitar a tomada de decisões estratégicas. A escolha das cores e a interatividade dos gráficos permitem uma navegação intuitiva e personalizada.
    </br></br>
    <b>Observação</b>: Somente é aceito carga de arquivos CSV, você deve essolher o separador utilizado no arquivo. Ao utilizar dados do DataRio pode ser necessário tratamento anterior para possibilitar a carga correta dos dados.
</div>
""", unsafe_allow_html=True)

# Seção do "Dashboard de Dados" também usando markdown
st.markdown(f"<h1 style='color: {text_color};'>Dashboard de Turismo - Rio de Janeiro</h1>", unsafe_allow_html=True)

# Opção para o usuário escolher o separador do CSV
st.markdown(f"<h3 style='color: {text_color};'>Escolha o separador do arquivo CSV:</h3>", unsafe_allow_html=True)
separator = st.radio("Selecione o separador do arquivo CSV:", options=[",", ";", "|", "\t"], index=0)

# Carregar arquivo CSV
st.markdown(f"<h3 style='color: {text_color};'>Faça o upload do arquivo CSV de turismo:</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

# Verifica se o arquivo foi carregado
if uploaded_file is not None:
    # Carrega os dados utilizando cache
    df = load_data(uploaded_file, separator)

    # Filtros por colunas
    st.sidebar.subheader("Seleção de Colunas:")
    all_columns = df.columns.tolist()

    # Dropdown para seleção de colunas
    selected_columns = st.sidebar.multiselect("Selecione as colunas que deseja visualizar:", all_columns, default=all_columns)

    # Filtragem por valores e persistência no Session State
    st.sidebar.subheader("Filtros de Dados:")
    display_option = st.sidebar.radio("Selecione o que deseja visualizar:", ("Todos os dados", "Filtrar por coluna específica"))

    if display_option == "Filtrar por coluna específica":
        column_to_filter = st.sidebar.selectbox("Selecione a coluna para aplicar o filtro:", all_columns)
        if df[column_to_filter].dtype == 'object':
            unique_values = df[column_to_filter].unique()
            selected_value = st.sidebar.selectbox(f"Selecione o valor da coluna '{column_to_filter}'", unique_values)
            st.session_state["filtered_data"] = df[df[column_to_filter] == selected_value]
        else:
            min_value = df[column_to_filter].min()
            max_value = df[column_to_filter].max()
            selected_range = st.sidebar.slider(f"Selecione o intervalo de {column_to_filter}", min_value, max_value, (min_value, max_value))
            st.session_state["filtered_data"] = df[(df[column_to_filter] >= selected_range[0]) & (df[column_to_filter] <= selected_range[1])]
    else:
        st.session_state["filtered_data"] = df[selected_columns]

    # Exibição da tabela interativa
    st.markdown(f"<h3 style='color: {text_color};'>Dados Carregados</h3>", unsafe_allow_html=True)
    st.write("Visualização dos primeiros registros:")
    st.dataframe(st.session_state["filtered_data"])

    # Serviço de Download de Arquivos
    st.markdown(f"<h3 style='color: {text_color};'>Baixar Dados Filtrados</h3>", unsafe_allow_html=True)
    csv_data = st.session_state["filtered_data"].to_csv(index=False)
    st.download_button(label="Baixar CSV", data=csv_data, file_name="dados_turismo_filtrados.csv", mime="text/csv")

    # Exibir Métricas Básicas
    st.markdown(f"<h3 style='color: {text_color};'>Métricas Básicas</h3>", unsafe_allow_html=True)

    # Filtra apenas colunas numéricas
    numeric_data = st.session_state["filtered_data"].select_dtypes(include=['number'])

    # Verifica se existem colunas numéricas antes de exibir as métricas
    if not numeric_data.empty:
        st.write("Contagem de registros:", len(st.session_state["filtered_data"]))
        st.write("Médias das colunas numéricas:")
        st.write(numeric_data.mean())
    else:
        st.warning("Nenhuma coluna numérica disponível para calcular métricas.")

    # Visualizações de Dados - Gráficos Simples
    st.markdown(f"<h3 style='color: {text_color};'>Visualizações Simples</h3>", unsafe_allow_html=True)
    chart_type = st.selectbox("Selecione o tipo de gráfico:", ["Barras", "Linhas", "Pizza"])

    if chart_type == "Barras":
        fig = px.bar(st.session_state["filtered_data"], x=st.session_state["filtered_data"].columns[0], y=st.session_state["filtered_data"].columns[1])
        st.plotly_chart(fig)
    elif chart_type == "Linhas":
        fig = px.line(st.session_state["filtered_data"], x=st.session_state["filtered_data"].columns[0], y=st.session_state["filtered_data"].columns[1])
        st.plotly_chart(fig)
    elif chart_type == "Pizza":
        fig = px.pie(st.session_state["filtered_data"], names=st.session_state["filtered_data"].columns[0], values=st.session_state["filtered_data"].columns[1])
        st.plotly_chart(fig)

    # Visualizações de Dados - Gráficos Avançados
    st.markdown(f"<h3 style='color: {text_color};'>Visualizações Avançadas</h3>", unsafe_allow_html=True)
    adv_chart_type = st.selectbox("Selecione o gráfico avançado:", ["Histograma", "Scatter Plot"])

    if adv_chart_type == "Histograma":
        fig, ax = plt.subplots()
        ax.hist(numeric_data[numeric_data.columns[0]], bins=20)
        st.pyplot(fig)
    elif adv_chart_type == "Scatter Plot":
        fig = px.scatter(st.session_state["filtered_data"], x=st.session_state["filtered_data"].columns[0], y=st.session_state["filtered_data"].columns[1])
        st.plotly_chart(fig)

else:
    st.warning("Por favor, faça o upload de um arquivo CSV.")
