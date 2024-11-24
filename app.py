import streamlit as st

# Configurações iniciais da página
st.set_page_config(
    page_title="ZAedes - Monitoramento",
    layout="wide",
)

# Título principal
st.title("Bem-vindo ao ZAedes")
st.write("""
Utilizando aprendizado de máquina e big data para monitorar e prevenir surtos de doenças causadas pelo mosquito Aedes aegypti.
""")

# Menu lateral
menu = st.sidebar.radio(
    "Menu",
    ["Dashboard", "Mapa de Risco", "Notificações", "Administração"]
)

# Navegação entre páginas
if menu == "Dashboard":
    from Dashboard import main as dashboard
    dashboard()
elif menu == "Mapa de Risco":
    from Risk_Map import main as risk_map
    risk_map()
elif menu == "Notificações":
    from Notifications import main as notifications
    notifications()
elif menu == "Administração":
    from Admin import main as admin
    admin()




