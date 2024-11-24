import pandas as pd
import folium
from streamlit_folium import st_folium
import streamlit as st

def main():
    st.title("Mapa de Risco")

    # Carregar os dados do CSV
    data = pd.read_csv("data/fake_data.csv")

    # Criar o mapa centrado em Feira de Santana
    m = folium.Map(location=[-12.266, -38.966], zoom_start=12)

    for _, row in data.iterrows():
        # Determinar a cor com base no risco
        color = "red" if row["Risco"] == "Alto" else "orange" if row["Risco"] == "Médio" else "green"
        
        # Adicionar marcadores com dados fictícios
        folium.Circle(
            location=[-12.266 + (row.name * 0.01), -38.966 + (row.name * 0.01)],  # Coordenadas ajustadas para simulação
            radius=row["Casos"] * 10,
            color=color,
            fill=True,
            fill_opacity=0.6,
            popup=f"{row['Area']} - Risco: {row['Risco']} ({row['Casos']} casos)",
        ).add_to(m)

    # Renderizar o mapa no Streamlit
    st_folium(m, width=700, height=500)


