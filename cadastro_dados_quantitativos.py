import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Cadastro de Dados Quantitativos - FIDCs", layout="centered")
st.title("📥 Cadastro de Dados Quantitativos – FIDCs")

# Caminhos dos arquivos
ARQUIVO_LOG = "logs/atividade_usuarios.csv"
ARQUIVO_DADOS = "dados_fidcs.csv"

os.makedirs("logs", exist_ok=True)

# Login
st.sidebar.title("🔐 Login do Usuário")
usuario = st.sidebar.text_input("Nome do Usuário")
funcao = st.sidebar.selectbox("Função", ["Riscos", "Compliance", "Aprovador", "Operacional"])

if usuario and funcao:
    st.success(f"Usuário logado como {usuario} ({funcao})")

    if os.path.exists(ARQUIVO_LOG):
        log_usuarios = pd.read_csv(ARQUIVO_LOG, sep=';', decimal=',')
    else:
        log_usuarios = pd.DataFrame(columns=["Timestamp", "Usuário", "Função", "Ação", "Fundo", "DtReferencia", "Detalhes"])

    st.markdown("""
    Faça o upload do arquivo contendo os dados operacionais dos FIDCs (formato CSV com ponto e vírgula).
    O sistema registrará a operação com identificação do usuário e data/hora.
    """)

    arquivo = st.file_uploader("📁 Upload do arquivo de dados quantitativos", type="csv")

    if arquivo:
        df_novo = pd.read_csv(arquivo, sep=';', decimal=',')

        if os.path.exists(ARQUIVO_DADOS):
            df_antigo = pd.read_csv(ARQUIVO_DADOS, sep=';', decimal=',')
            df_merged = pd.concat([df_antigo, df_novo], ignore_index=True)
        else:
            df_merged = df_novo.copy()

        df_merged.to_csv(ARQUIVO_DADOS, sep=';', decimal=',', index=False)

        # Log por fundo
        fundos = df_novo["NmFundo"].unique()
        data_ref = df_novo["DtReferencia"].unique()

        for fundo in fundos:
            for data in data_ref:
                log_usuarios = pd.concat([log_usuarios, pd.DataFrame([{
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Usuário": usuario,
                    "Função": funcao,
                    "Ação": "Cadastro Quantitativo",
                    "Fundo": fundo,
                    "DtReferencia": data,
                    "Detalhes": f"Linhas inseridas: {len(df_novo[df_novo['NmFundo'] == fundo])}"
                }])], ignore_index=True)

        log_usuarios.to_csv(ARQUIVO_LOG, sep=';', decimal=',', index=False)

        st.success(f"Upload realizado com sucesso. Dados salvos e log registrado para {len(fundos)} fundos.")
        st.dataframe(df_novo.head())
else:
    st.warning("⚠️ Faça login preenchendo nome e função na barra lateral para continuar.")
