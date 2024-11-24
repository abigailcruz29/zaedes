import pandas as pd
import streamlit as st

def main():
    st.title("Dashboard")

    # Carregar os dados do CSV
    data = pd.read_csv("data/fake_data.csv")

    # Exibir tabela
    st.subheader("Dados Brutos")
    st.write(data)

    # Exemplo de gráfico de casos por área
    st.subheader("Casos por Área")
    st.bar_chart(data.set_index("Area")["Casos"])

