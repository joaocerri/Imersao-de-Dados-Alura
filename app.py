import streamlit as st
import pandas as pd
import plotly.express as px

# URL do dataset da imersão
DATA_URL = "https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    return df

df = load_data()

st.title("📊 Dashboard - Análise de Salários em Data Jobs")
st.markdown("Exploração interativa dos dados de salários na área de tecnologia (base da imersão Alura).")

# Filtros na barra lateral
st.sidebar.header("Filtros")

# Remover NaNs dos filtros
anos = sorted(df["work_year"].dropna().unique())
cargos = sorted(df["job_title"].dropna().unique())
senioridade = sorted(df["experience_level"].dropna().unique())
local = sorted(df["company_location"].dropna().unique())

# Filtros com valores padrão
anos_default = anos
cargos_default = ["Data Scientist", "Data Engineer", "Machine Learning Engineer"]
senioridade_default = senioridade
local_default = local

anos = st.sidebar.multiselect("Ano", options=anos, default=anos_default)
cargos = st.sidebar.multiselect("Cargo", options=cargos, default=cargos_default)
senioridade = st.sidebar.multiselect("Nível de Senioridade", options=senioridade, default=senioridade_default)
local = st.sidebar.multiselect("Local da Empresa", options=local, default=local_default)

df_filtered = df[
    (df["work_year"].isin(anos)) &
    (df["job_title"].isin(cargos)) &
    (df["experience_level"].isin(senioridade)) &
    (df["company_location"].isin(local))
]

# KPIs
st.subheader("📌 Indicadores Gerais")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Média Salarial (USD)", f"${df_filtered['salary_in_usd'].mean():,.0f}")
col2.metric("Mediana Salarial (USD)", f"${df_filtered['salary_in_usd'].median():,.0f}")
col3.metric("Salário Máximo (USD)", f"${df_filtered['salary_in_usd'].max():,.0f}")
col4.metric("Salário Mínimo (USD)", f"${df_filtered['salary_in_usd'].min():,.0f}")

# Gráficos
st.subheader("📈 Análises Visuais")

fig1 = px.bar(
    df_filtered.groupby("job_title")["salary_in_usd"].mean().sort_values(ascending=False).head(10).reset_index(),
    x="salary_in_usd", y="job_title", orientation="h",
    title="Salário Médio por Cargo"
)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.box(
    df_filtered, x="experience_level", y="salary_in_usd",
    title="Distribuição de Salário por Senioridade"
)
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.pie(df_filtered, names="remote_ratio", title="Distribuição de Trabalho Remoto (%)")
st.plotly_chart(fig3, use_container_width=True)

fig4 = px.line(
    df_filtered.groupby("work_year")["salary_in_usd"].mean().reset_index(),
    x="work_year", y="salary_in_usd", markers=True,
    title="Evolução do Salário Médio por Ano"
)
st.plotly_chart(fig4, use_container_width=True)
