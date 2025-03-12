import streamlit as st
import pandas as pd
import plotly.express as px
import math

st.set_page_config(layout="wide")

# Mostrar qual mês teve o maior número de vendas 
# um gráfico de linhas com o total de vendas em cada mes FEITO
# gráfico de barras horizontal com os modelos de cada marca e qual vendeu mais (maior ao menor)
# Filtros de ano, tipos de carro, tipo de cambio, genero(com opção de All)
# talvez um de pizza por porcentagem de cor de carros mais vendidas FEITO
# em cima quantidate total de vendas, preço médio de carro, total de vendas em $, e total de carros automatico e manuais(número total e do lado a porcentagem entre os dois)

df = pd.read_csv("car sales.csv")

# Tratamento dos dados
df = df.drop(columns=["Customer Name", "Dealer_Name", "Phone", "Dealer_No "])
# print(df.isnull().sum())
# print(df.duplicated().sum())

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

st.sidebar.header("Câmbio")
all_cambio = st.sidebar.checkbox("All",key="cambio", value=True)
filter_manual = st.sidebar.checkbox("Manual", value=all_cambio, disabled=all_cambio)
filter_auto = st.sidebar.checkbox("Automático", value=all_cambio, disabled=all_cambio)

if all_cambio or (not filter_manual and not filter_auto):
    df_filtered = df_filtered
else:
    selected_cambio = []
    if filter_manual:
        selected_cambio.append("Manual")
    if filter_auto:
        selected_cambio.append("Auto")
    
    df_filtered = df_filtered[df_filtered["Transmission"].isin(selected_cambio)]


# df_filtered

us_locations = {
    "Austin": {"lat": 30.2672, "lon": -97.7431},
    "Janesville": {"lat": 42.6828, "lon": -89.0187},
    "Scottsdale": {"lat": 33.4942, "lon": -111.9261},
    "Pasco": {"lat": 46.2396, "lon": -119.1006},
    "Aurora": {"lat": 39.7294, "lon": -104.8319},
    "Middletown": {"lat": 39.5151, "lon": -84.3983},
    "Greenville": {"lat": 34.8526, "lon": -82.3940}
}
df_sales = df.groupby("Dealer_Region", as_index=False).agg({"Price ($)": "sum"})
df_sales["lat"] = df_sales["Dealer_Region"].map(lambda x: us_locations.get(x, {}).get("lat"))
df_sales["lon"] = df_sales["Dealer_Region"].map(lambda x: us_locations.get(x, {}).get("lon"))
df_sales = df_sales.dropna()
df_sales["formatted_price"] = df_sales["Price ($)"].apply(lambda x: f"${x/1_000_000:.1f}M" if x >= 1_000_000 else f"${x}")

col1, col2, col3, col4, col5 = st.columns(5)
col6, col7 ,col8 = st.columns(3)
col9, col10 = st.columns(2)

sales_t=df["Car_id"].count().sum()
col1.metric(label="Quantidade de Vendas", value=f"{sales_t:,.0f}", border=True)

media = df["Price ($)"].mean()
media=round(media)
col2.metric(label="Preço Médio", value=f"$ {media:,.0f}", border = True)

total = df["Price ($)"].sum()
total=round(total)
total_m = math.ceil(total/1_000_000)
col3.metric(label="Total de Vendas", value=f"$ {total_m:,.0f} M", border=True)

cambio = df["Transmission"].value_counts()
cambio_porcento = df["Transmission"].value_counts(normalize=True) * 100
col4.metric(label="Carro Automático", value=f"{cambio['Auto']:,.0f}",delta= f"{cambio_porcento['Auto']:.2f}%" ,delta_color="normal" ,border=True)
col5.metric(label="Carro Manual", value=f"{cambio['Manual']:,.0f}",delta= f"{cambio_porcento['Manual']:.2f}%" , delta_color="inverse",border=True)


month_total = df_filtered.groupby("Month")[["Price ($)"]].sum().reset_index()
month_total["Month"] = pd.to_datetime(month_total["Month"])
month_total = month_total.sort_values("Month")
fig_line = px.line(month_total, x="Month", y="Price ($)"   
                   , title="Venda de Carros por Mês", markers=True)
fig_line.update_traces(line=dict(color="rgba(255, 0, 0, 0.5)")) 
fig_line.update_traces(marker=dict(color="rgba(255, 0, 0, 0.5)", size=8))
fig_line.update_traces(fill="tozeroy", fillcolor="rgba(0, 0, 255, 0.2)") 
col6.plotly_chart(fig_line, use_container_width=True)

car_colors = df.groupby("Color")[["Car_id"]].count().reset_index()
fig_color = px.pie(car_colors, values="Car_id", names="Color", 
                   title= "Distribuição de Vendas por Cor", color="Color")
col7.plotly_chart(fig_color, use_container_width=True)

caroc_regi = df.groupby(["Dealer_Region", "Body Style"]).size().reset_index(name="Count")
fig_regi = px.bar(caroc_regi, x="Dealer_Region", y="Count", color="Body Style",
                  title="Distribuição de Carrocerias por Região", labels={"Count": "Número de Carros", "Dealer_Region": "Região"})
col8.plotly_chart(fig_regi, use_container_width=True)

df_grouped = df_filtered.groupby(['Company'], as_index=False)['Price ($)'].sum()
fig_model = px.bar(df_grouped, 
             x='Price ($)', 
             y='Company', 
             color='Company', 
             orientation='h',
             title='Preços Total de Venda dos Carros por Marca ',
             labels={'Price ($)': 'Preço ($)', 'Company': 'Marca', 'Model': 'Modelo'},
             height=600)             
col9.plotly_chart(fig_model, use_container_width=True)

fig_sales = px.scatter_geo(df_sales, lat="lat", lon="lon", size="Price ($)",
                            text="formatted_price", scope="usa",
                            title="Total de Vendas por Região",projection="albers usa",
                            height=600, size_max=50)
fig_sales.update_traces(textfont=dict(size=16, color="black"))
col10.plotly_chart(fig_sales, use_container_width=True)