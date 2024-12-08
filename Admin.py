import streamlit as st
import pandas as pd

# Função para exibir lista de usuários
def exibir_usuarios():
    # Dados fictícios de usuários
    usuarios = [
        {"ID": 1, "Nome": "Admin", "Email": "admin@exemplo.com", "Permissão": "Administrador"},
        {"ID": 2, "Nome": "Usuário A", "Email": "usuarioa@exemplo.com", "Permissão": "Usuário"},
        {"ID": 3, "Nome": "Usuário B", "Email": "usuariob@exemplo.com", "Permissão": "Usuário"},
    ]
    
    usuarios_df = pd.DataFrame(usuarios)
    
    st.write("### Lista de Usuários")
    st.dataframe(usuarios_df)

# Função para gerenciar permissões de usuários
def gerenciar_permissoes():
    st.write("### Gerenciamento de Permissões")
    
    permissao = st.selectbox("Selecione a permissão", ["Administrador", "Usuário", "Convidado"])
    nome_usuario = st.text_input("Nome do Usuário", "")
    email_usuario = st.text_input("E-mail do Usuário", "")
    
    if st.button("Atualizar Permissão"):
        if nome_usuario and email_usuario:
            st.success(f"Permissão do usuário {nome_usuario} ({email_usuario}) foi atualizada para {permissao}.")
        else:
            st.error("Por favor, preencha os campos de Nome e E-mail.")

# Função para editar configurações do sistema
def editar_configuracoes():
    st.write("### Configurações do Sistema")
    
    limite_alerta = st.number_input("Limite de Alerta de Casos", min_value=0, value=1000)
    limite_previsao = st.number_input("Limite de Casos Previstos", min_value=0, value=1500)
    
    if st.button("Salvar Configurações"):
        st.success(f"Configurações salvas: Limite de Alerta = {limite_alerta}, Limite de Previsão = {limite_previsao}")

# Função para mostrar opções do seletor (selectbox) dentro da página
def mostrar_opcoes():
    st.write("### Selecione uma opção para gerenciar")

    # Seletor de opções dentro da página principal (não na barra lateral)
    opcao_selecionada = st.selectbox(
        "Escolha uma funcionalidade",
        ["Configurações", "Gerenciar Usuários", "Gerenciar Permissões"]
    )
    
    # Exibindo o conteúdo baseado na escolha do selectbox
    if opcao_selecionada == "Configurações":
        editar_configuracoes()
    
    elif opcao_selecionada == "Gerenciar Usuários":
        exibir_usuarios()
    
    elif opcao_selecionada == "Gerenciar Permissões":
        gerenciar_permissoes()

# Função principal de administração
def main():
    st.title("Administração")
    st.write("Configurações e Gerenciamento de Usuários")
    
    # Chama a função que mostra as opções de gerenciamento
    mostrar_opcoes()

if __name__ == "__main__":
    main()