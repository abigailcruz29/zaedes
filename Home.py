import streamlit as st

def main():

    # Título do projeto
    st.title("🦟 Prevenção de Doenças do Aedes aegypti")

    # Subtítulo
    st.subheader("Usando Inteligência Artificial e Big Data para proteger a saúde pública")

    # Descrição do projeto
    st.write(
        """
        Este projeto utiliza tecnologias avançadas, como Inteligência Artificial e Big Data, 
        para monitorar e prevenir epidemias de doenças transmitidas pelo mosquito Aedes aegypti, 
        como dengue, zika e chikungunya. Aqui você pode explorar dados, visualizar análises e 
        entender as estratégias implementadas para reduzir a incidência dessas doenças.
        """
    )

    # Seção para inserção de informações extras
    st.markdown("### Dados e Informações")
    st.write(
        """
        - **Casos monitorados:** 10.000+
        - **Áreas cobertas:** Regiões urbanas e rurais
        - **Ferramentas utilizadas:** Modelos de predição, mapas de calor e alertas em tempo real
        """
    )

    # Botões para navegação ou interação
    if st.button("Explorar Dados"):
        st.write("Aqui será exibida uma seção com gráficos e tabelas de dados!")

    if st.button("Sobre o Projeto"):
        st.write(
            """
            Este projeto é uma iniciativa colaborativa entre pesquisadores, autoridades de saúde pública 
            e desenvolvedores, com foco em melhorar a qualidade de vida por meio da tecnologia.
            """
        )

    # Rodapé
    st.markdown("---")
    st.markdown("© 2024 - Projeto Aedes aegypti AI. Todos os direitos reservados.")

if __name__ == "__main__":
    main()