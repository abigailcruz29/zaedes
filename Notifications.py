import pandas as pd
import streamlit as st
import requests
import matplotlib.pyplot as plt

def gerar_notificacoes(historicos_df, previsoes_df, limite_alto=1000, limite_previsao=1500):
    """
    Função para gerar notificações com base nos dados históricos e previsões.
    """
    notificacoes = []

    # Notificação para altos casos históricos
    if historicos_df["Casos Totais"].max() > limite_alto:
        notificacoes.append({
            "Mensagem": f"Altos casos históricos detectados: {historicos_df['Casos Totais'].max()} casos em 2024.",
            "Nível": "Alto"
        })

    # Comparação entre o máximo de 2024 e a previsão de 2025
    max_2024 = historicos_df["Casos Totais"].max()
    max_2025 = previsoes_df["Casos Previstos"].max()
    if max_2025 > max_2024:
        notificacoes.append({
            "Mensagem": f"A previsão para 2025 é alarmante, com {max_2025} casos previstos, superando os {max_2024} casos registrados em 2024.",
            "Nível": "Alto"
        })
    else:
        notificacoes.append({
            "Mensagem": f"A previsão de casos para 2025 ({max_2025} casos) é menor que o número de casos registrados em 2024 ({max_2024} casos).",
            "Nível": "Médio"
        })

    # Tendência de casos - comparação mês a mês
    if len(historicos_df) > 1:
        # Calcular a diferença entre o último mês e o mês anterior
        ultima_diferença = historicos_df["Casos Totais"].diff().iloc[-1]  # Diferença entre o último mês e o anterior
        if ultima_diferença > 0:
            notificacoes.append({
                "Mensagem": f"Tendência de aumento nos casos: aumento de {ultima_diferença} casos do último mês.",
                "Nível": "Médio"
            })
        elif ultima_diferença < 0:
            notificacoes.append({
                "Mensagem": f"Tendência de queda nos casos: redução de {abs(ultima_diferença)} casos do último mês.",
                "Nível": "Baixo"
            })
        else:
            notificacoes.append({
                "Mensagem": "Os casos estão estáveis, sem variação significativa nos últimos meses.",
                "Nível": "Baixo"
            })

    # Notificação sobre possíveis surtos baseados em aumento rápido
    if historicos_df["Casos Totais"].iloc[-3:].sum() > limite_alto:
        notificacoes.append({
            "Mensagem": "Alerta: possível surto, com um aumento significativo nos últimos 3 meses.",
            "Nível": "Alto"
        })

    return notificacoes

def plotar_grafico(historicos_df, previsoes_df):
    """
    Função para plotar o gráfico de casos históricos de 2024 e previsões de 2025.
    """
    plt.figure(figsize=(10, 6))

    # Gráfico de casos históricos de 2024
    plt.plot(historicos_df['Mês'], historicos_df['Casos Totais'], label='Casos Totais 2024', marker='o', color='blue')

    # Gráfico de casos previstos para 2025
    plt.plot(previsoes_df['Mês'], previsoes_df['Casos Previstos'], label='Casos Previstos 2025', marker='x', color='orange')

    # Título e rótulos
    plt.title("Casos de Doenças: 2024 (Histórico) vs 2025 (Previsões)")
    plt.xlabel("Mês")
    plt.ylabel("Número de Casos")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()

    # Exibir gráfico
    st.pyplot(plt)

def main():
    st.title("Notificações de Casos de Doenças")

    # Seletor para escolher a doença
    doencas = ["dengue", "zika", "chikungunya"]
    doenca_selecionada = st.selectbox("Escolha a Doença", doencas)

    # Configuração da requisição à API
    url = "https://restic-app-predicao.koyeb.app/predicao/"
    payload = {
        "geocodigo": 2910800,  # Exemplo para Feira de Santana, BA
        "doenca": doenca_selecionada,  # Doença escolhida pelo usuário
        "ano_inicio": 2015,
        "ano_fim": 2024
    }

    # Requisição à API
    with st.spinner("Carregando dados..."):
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Lança erro se a requisição falhar
            dados_api = response.json()

            # Processando os dados históricos para 2024
            historicos = [
                {"Ano": item["ano"], "Mês": item["mes"], "Casos Totais": item["casos_totais"], "Casos Previstos": item["casos_previstos"]}
                for item in dados_api["prediction"]["dados_historicos"]
                if item["ano"] == 2024  # Filtrando para o ano de 2024
            ]
            historicos_df = pd.DataFrame(historicos)

            # Processando as previsões futuras para 2025
            previsoes = [
                {"Ano": item["ano"], "Mês": item["mes"], "Casos Previstos": item["casos_previstos"]}
                for item in dados_api["prediction"]["previsoes"]
            ]
            previsoes_df = pd.DataFrame(previsoes)

            st.success("Dados carregados com sucesso!")

            # Gerar notificações dinâmicas com base nos dados
            notificacoes = gerar_notificacoes(historicos_df, previsoes_df)

            # Resumo Geral
            st.markdown("### Resumo Geral")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Máximo de Casos Históricos (2024)", historicos_df["Casos Totais"].max())
            with col2:
                st.metric("Máximo de Casos Previstos (2025)", previsoes_df["Casos Previstos"].max())

            # Notificações
            st.markdown("### Notificações")
            for n in notificacoes:
                if n["Nível"] == "Alto":
                    st.error(f"**{n['Nível']}** - {n['Mensagem']}")
                elif n["Nível"] == "Médio":
                    st.warning(f"**{n['Nível']}** - {n['Mensagem']}")
                else:
                    st.info(f"**{n['Nível']}** - {n['Mensagem']}")

            # Exibir gráfico com casos históricos e previsões
            st.markdown("### Gráfico de Casos Históricos de 2024 e Previsões de 2025")
            plotar_grafico(historicos_df, previsoes_df)

        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao conectar à API: {e}")
        except KeyError as e:
            st.error(f"Erro ao processar a resposta da API: {e}")

if __name__ == "__main__":
    main()