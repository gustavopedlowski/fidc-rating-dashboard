import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Cadastro de Score Estrutural - FIDCs")
st.title("📝 Cadastro de Score Estrutural por Fundo")

ARQUIVO_HISTORICO = "historico_scores_estruturais.csv"

# Verifica se já existe histórico
if os.path.exists(ARQUIVO_HISTORICO):
    historico = pd.read_csv(ARQUIVO_HISTORICO, sep=';', decimal=',')
else:
    historico = pd.DataFrame(columns=[
        "NmFundo", "DtReferencia",
        "Qualidade Originador", "Contratos", "Histórico Inadimplência",
        "Concentração", "Governança", "Garantias"
    ])

st.markdown("""
Selecione o fundo e insira as notas qualitativas (de 0 a 5) com base na metodologia interna da Catálise Investimentos.
Cada nota será salva com data e poderá ser usada no cálculo do rating final.
""")

# Inputs principais
fundos_unicos = sorted(historico["NmFundo"].unique().tolist())
novo_fundo = st.text_input("Novo Fundo (ou selecione abaixo):")
fundo = novo_fundo if novo_fundo else st.selectbox("Fundo existente:", options=fundos_unicos)

mes = st.date_input("Data de Referência", value=datetime.today()).strftime("%Y-%m")

# Notas qualitativas
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

if st.button("Salvar notas do fundo"):
    nova_linha = pd.DataFrame([{
        "NmFundo": fundo,
        "DtReferencia": mes,
        "Qualidade Originador": nota_or,
        "Contratos": nota_contratos,
        "Histórico Inadimplência": nota_hist,
        "Concentração": nota_conc,
        "Governança": nota_gov,
        "Garantias": nota_garantias
    }])

    historico = pd.concat([historico, nova_linha], ignore_index=True)
    historico.to_csv(ARQUIVO_HISTORICO, sep=';', decimal=',', index=False)
    st.success(f"Notas para o fundo '{fundo}' em {mes} foram salvas com sucesso.")

# Mostrar histórico recente
st.markdown("### Histórico Recentemente Registrado")
st.dataframe(historico.sort_values(by=["DtReferencia", "NmFundo"], ascending=False).tail(10))
