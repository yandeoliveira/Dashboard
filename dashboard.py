import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar o layout da página
st.set_page_config(page_title="Dashboard de Vendas", page_icon="📊",
                   layout="wide", initial_sidebar_state="expanded")

# Carregar os dados do arquivo "vendas.csv"
df = pd.read_csv("vendas.csv", sep=",", decimal=".")

# Remover espaços em branco dos nomes das colunas
df.columns = df.columns.str.strip()

# Verifique se a coluna 'data' existe
if 'data' in df.columns:
    # Converter a coluna "data" para o formato de data
    df["data"] = pd.to_datetime(df["data"])
    df = df.sort_values("data")

    # Criar uma nova coluna "Month" que contém o ano e o mês
    df["Month"] = df["data"].dt.to_period("M").astype(str)

    # Calcular o faturamento total do ano
    total_year_sales = df["valor_venda"].sum()

    # Calcular o faturamento total por mês
    monthly_sales = df.groupby("Month")[["valor_venda"]].sum().reset_index()
    monthly_sales.columns = ['Month', 'Total_Faturamento']

    # Criar uma seleção de meses na barra lateral do dashboard
    month = st.sidebar.selectbox(
        "Selecione o Mês", monthly_sales["Month"].unique())
    df_filtered = df[df["Month"] == month]

    # Filtro adicional para produtos
    product_filter = st.sidebar.multiselect(
        "Selecione os Produtos", df["produto"].unique())
    if product_filter:
        df_filtered = df_filtered[df_filtered["produto"].isin(product_filter)]

    # KPI: Faturamento Total do Ano e do Mês Selecionado
    total_month_sales = df_filtered["valor_venda"].sum()

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Faturamento Total do Ano",
                  value=f"R$ {total_year_sales:,.2f}")
    with col2:
        st.metric(label="Faturamento Total do Mês Selecionado",
                  value=f"R$ {total_month_sales:,.2f}")

    # Gráfico de faturamento por dia do mês selecionado
    fig_date = px.bar(df_filtered, x="data", y="valor_venda",
                      color="produto", title="Faturamento por dia do Mês Selecionado")
    fig_date.update_traces(marker=dict(
        line=dict(width=1, color='DarkSlateGrey')))
    st.plotly_chart(fig_date, use_container_width=True)

    # Calcular o faturamento total por produto
    product_total = df_filtered.groupby(
        "produto")[["valor_venda"]].sum().reset_index()

    # Criar o gráfico de barras para exibir o faturamento por produto
    fig_product = px.bar(product_total, x="produto",
                         y="valor_venda", title="Faturamento por produto")
    fig_product.update_traces(marker=dict(
        line=dict(width=1, color='DarkSlateGrey')))
    st.plotly_chart(fig_product, use_container_width=True)

    # Criar o gráfico de pizza para exibir o faturamento por tipo de produto
    fig_kind = px.pie(df_filtered, values="valor_venda",
                      names="produto", title="Faturamento por tipo de produto")
    st.plotly_chart(fig_kind, use_container_width=True)

    # Gráfico de tendência de faturamento do mês selecionado
    fig_trend = px.line(df_filtered, x="data", y="valor_venda",
                        title="Tendência de Faturamento do Mês Selecionado")
    st.plotly_chart(fig_trend, use_container_width=True)

    # Gráfico de faturamento total por mês do ano
    fig_monthly = px.bar(monthly_sales, x="Month", y="Total_Faturamento",
                         title="Faturamento Total por Mês do Ano")
    fig_monthly.update_traces(marker=dict(
        line=dict(width=1, color='DarkSlateGrey')))
    st.plotly_chart(fig_monthly, use_container_width=True)

    # Seção de feedback
    st.sidebar.header("Instruções")
    st.sidebar.write("Use os filtros na barra lateral para explorar os dados.")
    feedback = st.sidebar.text_area("Deixe seu feedback:")
    if st.sidebar.button("Enviar"):
        st.sidebar.success("Obrigado pelo seu feedback!")

else:
    st.error("A coluna 'data' não foi encontrada no arquivo CSV.")
