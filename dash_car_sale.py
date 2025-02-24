import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Mostrar qual mês teve o maior número de vendas
# um gráfico de linhas com o total de vendas em cada mes
# gráfico de barras horizontal com os modelos de cara marca e qual vendeu mais (maior ao menor)
#Filtros de ano, tipos de carro, tipo de cambio, genero, cor (com opção de All)
# talvez um de pizza por porcentagem de cor de carros mais vendidas
# em cima quantidate total de vendas, preço médio de carro, total de vendas em $, e total de carros automatico e manuais(número total e do lado a porcentagem entre os dois)

df = pd.read_csv("car sales.csv")


# Vendo o tipo de uma cloluna
# print(df["Date"].dtype)
# Muda o tipo do data de object para datetime
df["Date"] = pd.to_datetime(df["Date"])
# print(df["Date"].dtype)
df = df.sort_values("Date")

# cria uma nova coluna chamada year que contém só o valor dos meses para ser usado como filtro mais tarde 
df["Month"] = df["Date"].apply(lambda x : str(x.year) + "-" + str(x.month))


# cria uma nova coluna chamada year que contém só o valor dos anos para ser usado como filtro mais tarde 
df["Year"] = df["Date"].dt.year
# COM CHECKBOX
# Criar checkboxes para filtragem por ano
st.sidebar.header("Filtrar por Ano:")
filter_all = st.sidebar.checkbox("All", value=True)  # Começa marcado
filter_2022 = st.sidebar.checkbox("2022", value=filter_all, disabled=filter_all)
filter_2023 = st.sidebar.checkbox("2023", value=filter_all, disabled=filter_all)


# Aplicar o filtro no dataframe com base na seleção dos checkboxes
if filter_all or (not filter_2022 and not filter_2023):  # Se "All" for selecionado ou nenhum outro ano for marcado
    df_filtered = df
else:
    selected_years = []
    if filter_2022:
        selected_years.append(2022)
    if filter_2023:
        selected_years.append(2023)
    
    df_filtered = df[df["Year"].isin(selected_years)]

# Exibir o dataframe filtrado
df_filtered

col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)

month_total = df_filtered.groupby("Month")[["Price ($)"]].sum().reset_index()
month_total["Month"] = pd.to_datetime(month_total["Month"])
month_total = month_total.sort_values("Month")
fig_line = px.line(month_total, x="Month", y="Price ($)"   
                   , title="Venda de Carros por Mês", markers=True)
fig_line.update_traces(line=dict(color="rgba(255, 0, 0, 0.5)"))  # Vermelho com 70% de opacidade
fig_line.update_traces(marker=dict(color="rgba(255, 0, 0, 0.5)", size=8))
fig_line.update_traces(fill="tozeroy", fillcolor="rgba(0, 0, 255, 0.2)")  # Azul com transparência
col1.plotly_chart(fig_line, use_container_width=True)

car_colors = df.groupby("Color")[["Car_id"]].count().reset_index()
fig_color = px.pie(car_colors, values="Car_id", names="Color", 
                   title= "Distribuição de Vendas por Cor", color="Color")
col2.plotly_chart(fig_color, use_container_width=True)