import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuração inicial
st.set_page_config(page_title="Cadastro Estrutural com Login", layout="centered")
st.title("📝 Cadastro de Score Estrutural – FIDC")

# Arquivos
ARQUIVO_HISTORICO = "logs/historico_scores_estruturais.csv"
ARQUIVO_LOG = "logs/atividade_usuarios.csv"

os.makedirs("logs", exist_ok=True)

# Login do usuário
st.sidebar.title("🔐 Login do Usuário")
usuario = st.sidebar.text_input("Nome do Usuário")
funcao = st.sidebar.selectbox("Função", ["Riscos", "Compliance", "Aprovador", "Operacional"])

if usuario and funcao:
    st.success(f"Usuário logado como {usuario} ({funcao})")

    # Carrega histórico existente se houver
    if os.path.exists(ARQUIVO_HISTORICO):
        historico = pd.read_csv(ARQUIVO_HISTORICO, sep=';', decimal=',')
    else:
        historico = pd.DataFrame(columns=[
            "NmFundo", "DtReferencia",
            "Qualidade Originador", "Contratos", "Histórico Inadimplência",
            "Concentração", "Governança", "Garantias"
        ])

    if os.path.exists(ARQUIVO_LOG):
        log_usuarios = pd.read_csv(ARQUIVO_LOG, sep=';', decimal=',')
    else:
        log_usuarios = pd.DataFrame(columns=["Timestamp", "Usuário", "Função", "Ação", "Fundo", "DtReferencia", "Detalhes"])

    st.markdown("""
    Insira abaixo as notas qualitativas do fundo selecionado. As informações serão registradas com usuário, função e data/hora para controle de auditoria.
    """)

    fundos_disponiveis = sorted(historico["NmFundo"].unique().tolist())
    novo_fundo = st.text_input("Novo Fundo (ou selecione existente):")
    fundo = novo_fundo if novo_fundo else st.selectbox("Fundo existente:", options=fundos_disponiveis)
    dt_ref = st.date_input("Data de Referência", value=datetime.today()).strftime("%Y-%m")

    st.markdown("### Notas Qualitativas (0 a 5)")
    col1, col2 = st.columns(2)
    with col1:
        nota_or = st.slider("Qualidade Originador", 0, 5, 0)
        nota_contratos = st.slider("Contratos", 0, 5, 0)
        nota_hist = st.slider("Histórico Inadimplência", 0, 5, 0)
    with col2:
        nota_conc = st.slider("Concentração", 0, 5, 0)
        nota_gov = st.slider("Governança", 0, 5, 0)
        nota_garantias = st.slider("Garantias", 0, 5, 0)

    if st.button("Salvar Notas do Fundo"):
        nova_linha = pd.DataFrame([{
            "NmFundo": fundo,
            "DtReferencia": dt_ref,
            "Qualidade Originador": nota_or,
            "Contratos": nota_contratos,
            "Histórico Inadimplência": nota_hist,
            "Concentração": nota_conc,
            "Governança": nota_gov,
            "Garantias": nota_garantias
        }])

        historico = pd.concat([historico, nova_linha], ignore_index=True)
        historico.to_csv(ARQUIVO_HISTORICO, sep=';', decimal=',', index=False)

        log_linha = pd.DataFrame([{
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Usuário": usuario,
            "Função": funcao,
            "Ação": "Cadastro Estrutural",
            "Fundo": fundo,
            "DtReferencia": dt_ref,
            "Detalhes": "Notas estruturais registradas"
        }])

        log_usuarios = pd.concat([log_usuarios, log_linha], ignore_index=True)
        log_usuarios.to_csv(ARQUIVO_LOG, sep=';', decimal=',', index=False)

        st.success(f"Notas para o fundo '{fundo}' em {dt_ref} foram salvas com sucesso.")

    st.markdown("### Histórico Recente")
    st.dataframe(historico.sort_values(by=["DtReferencia", "NmFundo"], ascending=False).tail(10))
else:
    st.warning("⚠️ Faça login preenchendo nome e função na barra lateral para continuar.")

