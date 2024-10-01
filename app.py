# Descrição: Dashboard de vendas de um supermercado fictício. O dashboard é interativo e permite filtrar as vendas por cidade, tipo de cliente e gênero.
# O dashboard contém os seguintes KPIs:
# - Total de vendas
# - Avaliação média
# - Média de vendas por transação
# O dashboard também contém um gráfico de barras com as vendas por linha de produto.
# O dashboard foi desenvolvido em Python utilizando a biblioteca Streamlit.

# Libs utilizadas: pandas, plotly, streamlit
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
    
)

@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io='supermarkt_sales.xlsx',
        engine = 'openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows=1000,
    )
        
    # Adicionando a coluna 'hour' ao dataframe
    df['hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour
    return df

df = get_data_from_excel()

# ---- SIDEBAR ----#
st.sidebar.header("Por favor, filtre aqui:")
city = st.sidebar.multiselect(
    "Selecione a cidade:",
    options=df['City'].unique(),
    default=df['City'].unique()
)

customer_type = st.sidebar.multiselect(
    "Selecione o tipo de cliente:",
    options=df['Customer_type'].unique(),
    default=df['Customer_type'].unique()
)

gender = st.sidebar.multiselect(
    "Selecione o gênero:",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)


# ---- MAINPAGE ----#
st.title(":bar_chart: Sales Dashboard")
st.markdown("Este é um dashboard interativo para análise de vendas.")


# TOP KPI'S
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total de Vendas")
    st.title(f"R$ {total_sales:,}")
with middle_column:
    st.subheader("Avaliação Média")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Média de Vendas por Transação")
    st.subheader(f"R$ {average_sale_by_transaction}")

st.markdown("---")

# SALES BY PRODUCT LINES
sales_by_product_line = ( 
   df_selection.groupby(by=["Product line"]).sum(numeric_only=True)[["Total"]].sort_values(by="Total")
)

fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Vendas por Linha de Produto</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white"
)

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


# SALES BY HOUR
sales_by_hour = df_selection.groupby(by=["hour"]).sum(numeric_only=True)[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Vendas por Hora</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white"
)

fig_hourly_sales.update_layout(
    xaxis=(dict(tickmode="linear")),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

