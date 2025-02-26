import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Mostrar qual mês teve o maior número de vendas 
# um gráfico de linhas com o total de vendas em cada mes FEITO
# gráfico de barras horizontal com os modelos de cara marca e qual vendeu mais (maior ao menor)
# Filtros de ano, tipos de carro, tipo de cambio, genero, cor (com opção de All)
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
st.sidebar.header("Ano")
filter_all = st.sidebar.checkbox("All", key="year", value=True)  # Começa marcado
filter_2022 = st.sidebar.checkbox("2022", value=filter_all, disabled=filter_all)
filter_2023 = st.sidebar.checkbox("2023", value=filter_all, disabled=filter_all)
# Aplicar o filtro no dataframe com base na seleção dos checkboxes
if filter_all or (not filter_2022 and not filter_2023):  
    df_filtered = df
else:
    selected_years = []
    if filter_2022:
        selected_years.append(2022)
    if filter_2023:
        selected_years.append(2023)
    
    df_filtered = df[df["Year"].isin(selected_years)]

# Filtro por genero
st.sidebar.header("Gênero")
all_gender = st.sidebar.checkbox("All", key="gender", value=True)
filter_male = st.sidebar.checkbox("Homem", value=all_gender, disabled=all_gender)
filter_female = st.sidebar.checkbox("Mulher", value=all_gender, disabled=all_gender)


if all_gender or (not filter_male and not filter_female):
    df_filtered = df_filtered
else:
    selected_gender = []
    if filter_male:
        selected_gender.append("Male")
    if filter_female:
        selected_gender.append("Female")

    df_filtered = df_filtered[df_filtered["Gender"].isin(selected_gender)]


# Data Frame para usar caso utilize apenas o filtro de genero
# if all_gender or (not filter_male and not filter_female):
#     df_gender = df
# else:
#     selected_gender = []
#     if filter_male:
#         selected_gender.append("Male")
#     if filter_female:
#         selected_gender.append("Female")

#     df_gender = df[df["Gender"].isin(selected_gender)]


#filtro por tipo da carroceria
# hatchback, sedan, suv, hardtop, passenger.
st.sidebar.header("Carroceria")
all_body = st.sidebar.checkbox("All",key="body style", value=True)
filter_sedan = st.sidebar.checkbox("Sedan", value=all_body, disabled=all_body)
filter_hatchback = st.sidebar.checkbox("Hatchback", value=all_body, disabled=all_body)
filter_suv = st.sidebar.checkbox("SUV", value=all_body, disabled=all_body)
filter_hardtop = st.sidebar.checkbox("Hardtop", value=all_body, disabled=all_body)
filter_passenger = st.sidebar.checkbox("Passenger", value=all_body, disabled=all_body)

if all_body or (not filter_sedan and not filter_hatchback and not filter_suv and not filter_hardtop and not filter_passenger):
    df_filtered = df_filtered
else:
    selected_body = []
    if filter_sedan:
        selected_body.append("Sedan")
    if filter_hatchback:
        selected_body.append("Hatchback")
    if filter_suv:
        selected_body.append("SUV")
    if filter_hardtop:
        selected_body.append("Hardtop")   
    if filter_passenger:
        selected_body.append("Passenger")
    
    df_filtered = df_filtered[df_filtered["Body Style"].isin(selected_body)]

df_filtered

col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)

month_total = df_filtered.groupby("Month")[["Price ($)"]].sum().reset_index()
month_total["Month"] = pd.to_datetime(month_total["Month"])
month_total = month_total.sort_values("Month")
fig_line = px.line(month_total, x="Month", y="Price ($)"   
                   , title="Venda de Carros por Mês", markers=True)
fig_line.update_traces(line=dict(color="rgba(255, 0, 0, 0.5)")) 
fig_line.update_traces(marker=dict(color="rgba(255, 0, 0, 0.5)", size=8))
fig_line.update_traces(fill="tozeroy", fillcolor="rgba(0, 0, 255, 0.2)") 
col1.plotly_chart(fig_line, use_container_width=True)

car_colors = df.groupby("Color")[["Car_id"]].count().reset_index()
fig_color = px.pie(car_colors, values="Car_id", names="Color", 
                   title= "Distribuição de Vendas por Cor", color="Color")
col2.plotly_chart(fig_color, use_container_width=True)

