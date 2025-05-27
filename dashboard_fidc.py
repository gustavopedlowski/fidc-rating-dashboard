# Para executar este código, certifique-se de ter o Streamlit instalado com:
# pip install streamlit

try:
    import streamlit as st
except ModuleNotFoundError:
    raise ModuleNotFoundError("O pacote 'streamlit' não está instalado. Instale com 'pip install streamlit' e execute novamente.")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

st.set_page_config(page_title="Dashboard de Rating - FIDCs", layout="wide")
st.title("📊 Dashboard de Rating para FIDCs")

st.markdown("""
Este painel exibe a avaliação de risco dos FIDCs com base em análise estatística e PCA. 

Os scores são derivados de métricas operacionais e de risco, como PDD, Subordinação, Rentabilidade e outras.
""")

# Upload do arquivo
uploaded_file = st.file_uploader("📁 Faça upload do arquivo CSV de métricas dos FIDCs", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, sep=';', decimal=',')

    # Separar identificadores
    df_id = df[["NmFundo", "DtReferencia"]]
    df_corr = df.drop(columns=["NmFundo", "DtReferencia"], errors="ignore")

    # Imputar e padronizar
    df_corr.replace([np.inf, -np.inf], np.nan, inplace=True)
    imputer = SimpleImputer(strategy='median')
    df_corr = pd.DataFrame(imputer.fit_transform(df_corr), columns=df_corr.columns)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_corr)

    # PCA
    pca = PCA(n_components=X_scaled.shape[1])
    pca.fit(X_scaled)
    pc1_coefs = pca.components_[0]

    # Score
    df_score = df_id.copy()
    df_score["Score"] = -np.dot(X_scaled, pc1_coefs)
    df_score["Score"] = 100 * (df_score["Score"] - df_score["Score"].min()) / (df_score["Score"].max() - df_score["Score"].min())

    # Média por fundo
    df_media = df_score.groupby("NmFundo")["Score"].mean().reset_index().sort_values(by="Score", ascending=False)

    # Exibir tabela
    st.subheader("📈 Ranking dos Fundos por Score Médio")
    st.dataframe(df_media, use_container_width=True)

    # Gráfico de barras
    st.subheader("📉 Score Médio por Fundo")
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(data=df_media, x="Score", y="NmFundo", palette="Blues_d")
    ax.set_title("Ranking dos FIDCs por Score Médio")
    st.pyplot(fig)

    # Distribuição do Score
    st.subheader("📊 Distribuição dos Scores")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.histplot(df_score["Score"], bins=20, kde=True, color="royalblue")
    ax2.set_title("Distribuição dos Scores dos FIDCs")
    st.pyplot(fig2)

    # Métricas do PCA
    df_pesos = pd.DataFrame({"Métrica": df_corr.columns, "Coef_PC1": pc1_coefs})
    df_pesos["Peso_Abs"] = np.abs(df_pesos["Coef_PC1"])
    df_pesos["Peso_Normalizado"] = df_pesos["Peso_Abs"] / df_pesos["Peso_Abs"].sum()
    df_pesos = df_pesos.sort_values(by="Peso_Abs", ascending=False)

    st.subheader("⚖️ Importância das Métricas para o Score")
    st.dataframe(df_pesos[["Métrica", "Peso_Normalizado"]], use_container_width=True)

    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=df_pesos, x="Peso_Normalizado", y="Métrica", palette="Blues_d")
    ax3.set_title("Peso Normalizado das Métricas no PC1")
    st.pyplot(fig3)
else:
    st.warning("Faça upload de um arquivo CSV para visualizar o dashboard.")
