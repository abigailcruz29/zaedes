import pandas as pd
import streamlit as st
import requests

def main():
    # Layout do título e seletor
    col1, col2 = st.columns([4, 1])  # Dividindo o espaço em duas colunas
    with col1:
        st.title("Dashboard de Previsão de Doenças")
    with col2:
        # Seletor compacto no canto direito
        tipo_doenca = st.selectbox(
            "Tipo de Doença:",
            ["dengue", "zika", "chikungunya"],
            key="doenca_selector"
        )

    # Mapeamento dos números para os nomes dos meses em português
    meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho",
        7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }

    # Configuração da requisição à API
    url = "https://restic-app-predicao.koyeb.app/predicao/"
    payload = {
        "geocodigo": 2910800,
        "doenca": tipo_doenca,
        "ano_inicio": 2015,
        "ano_fim": 2024
    }

    # Função para formatar números com ponto para milhares e vírgula para decimais
    def formatar_numeros(df):
        return df.applymap(lambda x: f"{x:,.0f}".replace(",", ".") if isinstance(x, (int, float)) else x)

    with st.spinner("Carregando dados..."):
        try:
            # Chamada à API
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Lança erro se a requisição falhar
            dados_api = response.json()

            # Processando os dados históricos
            historicos = [
                {"Ano": item["ano"], "Mês": item["mes"], "Casos Totais": item["casos_totais"], "Casos Previstos": item["casos_previstos"]}
                for item in dados_api["prediction"]["dados_historicos"]
            ]
            historicos_df = pd.DataFrame(historicos)

            # Processando as previsões futuras
            previsoes = [
                {"Ano": item["ano"], "Mês": item["mes"], "Casos Previstos": item["casos_previstos"]}
                for item in dados_api["prediction"]["previsoes"]
            ]
            previsoes_df = pd.DataFrame(previsoes)

            st.success("Dados carregados com sucesso!")

            # Arredondando os casos previstos para facilitar a visualização
            historicos_df["Casos Previstos"] = historicos_df["Casos Previstos"].round()
            previsoes_df["Casos Previstos"] = previsoes_df["Casos Previstos"].round()

            # Convertendo o número do mês para o nome do mês em português
            historicos_df["Mês"] = historicos_df["Mês"].map(meses)
            previsoes_df["Mês"] = previsoes_df["Mês"].map(meses)

            # Filtro de ano para os dados históricos
            st.markdown("### Dados Históricos de Casos")
            ano_selecionado = st.selectbox(
                "Selecione o Ano:",
                sorted(historicos_df["Ano"].unique()),
                key="ano_selector"
            )

            # Filtrando os dados históricos pelo ano selecionado
            historicos_filtrados = historicos_df[historicos_df["Ano"] == ano_selecionado]

            # Remover a coluna "Ano" antes de exibir
            historicos_filtrados_sem_ano = historicos_filtrados.drop(columns=["Ano"])

            # Formatar e exibir tabela de dados históricos
            historicos_filtrados_sem_ano_formatado = formatar_numeros(historicos_filtrados_sem_ano)
            st.dataframe(historicos_filtrados_sem_ano_formatado, use_container_width=True, hide_index=True)

            # Preparando os dados para o gráfico com nomes dos meses
            historicos_filtrados["Data"] = pd.to_datetime(
                historicos_filtrados["Ano"].astype(str) + '-' +
                historicos_filtrados["Mês"].map({v: k for k, v in meses.items()}).astype(str) + '-1',
                format='%Y-%m-%d'
            )
            historicos_filtrados.set_index("Data", inplace=True)

            # Gráfico de casos históricos (duas linhas: reais e previstos)
            #st.markdown(f"### Gráfico de Casos Reais e Previstos para {ano_selecionado}")
            #st.line_chart(historicos_filtrados[["Casos Totais", "Casos Previstos"]])

            # Gráfico de casos históricos (duas linhas: reais e previstos)
            st.markdown(f"### Gráfico de Casos Reais e Previstos para {ano_selecionado}")
            tipo_grafico = st.radio("Escolha o tipo de gráfico:", ["Linha", "Barras"])
            if tipo_grafico == "Linha":
                st.line_chart(historicos_filtrados[["Casos Totais", "Casos Previstos"]])
            elif tipo_grafico == "Barras":
                st.bar_chart(historicos_filtrados[["Casos Totais", "Casos Previstos"]])

            # Adicionando uma divisória antes de "Previsões Futuras"
            st.divider()

            # Previsões futuras - Apenas ano 2025
            st.markdown("### Dados das Previsões Futuras de Casos de 2025")
            previsoes_2025 = previsoes_df[previsoes_df["Ano"] == 2025].drop(columns=["Ano"])  # Filtra para 2025 e remove o ano

            # Formatar e exibir tabela de previsões futuras
            previsoes_2025_formatado = formatar_numeros(previsoes_2025)
            st.dataframe(previsoes_2025_formatado, use_container_width=True, hide_index=True)

            # Preparando os dados para o gráfico de previsões futuras com nomes dos meses
            previsoes_2025["Data"] = pd.to_datetime(
                "2025" + '-' +
                previsoes_2025["Mês"].map({v: k for k, v in meses.items()}).astype(str) + '-1',
                format='%Y-%m-%d'
            )
            previsoes_2025.set_index("Data", inplace=True)

            # Gráfico de previsões futuras
            st.markdown("### Gráfico de Casos Previstos para 2025")
            st.line_chart(previsoes_2025["Casos Previstos"])

        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao conectar à API: {e}")
        except KeyError as e:
            st.error(f"Erro ao processar a resposta da API: {e}")

if __name__ == "__main__":
    main()