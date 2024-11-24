import streamlit as st

def main():
    st.title("Notificações")
    notifications = [
        {"Mensagem": "Alto risco de surto no Distrito Central", "Nível": "Alto"},
        {"Mensagem": "Novo caso reportado na Zona Leste", "Nível": "Médio"},
    ]

    for n in notifications:
        st.warning(f"**{n['Nível']}** - {n['Mensagem']}")
