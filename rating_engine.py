import pandas as pd
import numpy as np
import streamlit as st
import os
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

st.set_page_config(page_title="Rating Interno - FIDCs", layout="wide")
st.title("📊 Cálculo de Rating Interno – FIDCs")

# Arquivos
ARQ_OPERACIONAL = "dados_fidcs.csv"
ARQ_ESTRUTURAL = "logs/historico_scores_estruturais.csv"
ARQ_LOG = "logs/atividade_usuarios.csv"
ARQ_RESULTADO = "Rating_Interno_FIDCs_Resultados.csv"

os.makedirs("logs", exist_ok=True)

# Login
st.sidebar.title("🔐 Login do Usuário")
usuario = st.sidebar.text_input("Nome do Usuário")
funcao = st.sidebar.selectbox("Função", ["Riscos", "Compliance", "Aprovador", "Operacional"])

if usuario and funcao:
    st.success(f"Usuário logado como {usuario} ({funcao})")

    if not os.path.exists(ARQ_OPERACIONAL) or not os.path.exists(ARQ_ESTRUTURAL):
        st.warning("⚠️ É necessário que os arquivos de dados operacionais e estruturais existam.")
    else:
        # Carregar dados
        df_op = pd.read_csv(ARQ_OPERACIONAL, sep=';', decimal=',')
        df_es = pd.read_csv(ARQ_ESTRUTURAL, sep=';', decimal=',')

        col_id = ["NmFundo", "DtReferencia", "Tipo"]
        df_id = df_op[col_id]
        df_data = df_op.drop(columns=col_id, errors="ignore")

        imputer = SimpleImputer(strategy='median')
        df_data = pd.DataFrame(imputer.fit_transform(df_data), columns=df_data.columns)
        scaler = StandardScaler()
        df_scaled = pd.DataFrame(scaler.fit_transform(df_data), columns=df_data.columns)

        df_all = pd.concat([df_id.reset_index(drop=True), df_scaled], axis=1)

        # Pesos por tipo
        metricas_bf = {
            'A Vencer / PL (Presente)': 10,
            'Vencidos / PL (Presente)': 15,
            'PDD / PL': 11,
            'Prazo Médio Ponderado': 16,
            'Quantidade de Cedentes': 13,
            'Quantidade de Sacados': 7,
            'Quantidade de Títulos': 12,
            'Valor Médio dos Títulos': 0,
            'Índice de Subordinação': 4,
            'Rentabilidade Patrimonial Mensal': 2,
            'Desvio Padrão da Rentabilidade': 9
        }

        metricas_mm = {
            'A Vencer / PL (Presente)': 7.0,
            'Vencidos / PL (Presente)': 10.5,
            'PDD / PL': 7.7,
            'Prazo Médio Ponderado': 11.2,
            'Quantidade de Cedentes': 9.1,
            'Quantidade de Sacados': 4.9,
            'Quantidade de Títulos': 8.4,
            'Valor Médio dos Títulos': 0.0,
            'Índice de Subordinação': 2.8,
            'Rentabilidade Patrimonial Mensal': 1.4,
            'Desvio Padrão da Rentabilidade': 6.3,
            '% Maior Cedente / PL do Fundo': 6.0,
            '% Maior Cedente / PL da Subordinada Jr': 5.0,
            '% Maior Sacado / PL do Fundo': 6.0,
            '% Maior Sacado / PL da Subordinada Jr': 5.0,
            'Valor de Recompra / PL do Fundo': 4.0,
            'Valor de Recompra / PL da Subordinada Jr': 4.0
        }

        def calcular_score_quantitativo(row):
            tipo = row['Tipo']
            metricas = metricas_bf if tipo == 'BF' else metricas_mm
            score, total_peso = 0, 0
            for m, p in metricas.items():
                if m in row and not pd.isna(row[m]):
                    score += row[m] * p
                    total_peso += p
            return 100 * score / total_peso if total_peso > 0 else np.nan

        df_all['Score Quantitativo'] = df_all.apply(calcular_score_quantitativo, axis=1)

        # Estrutural
        df_all = df_all.merge(df_es, on=["NmFundo", "DtReferencia"], how="left")
        col_qualitativas = ["Qualidade Originador", "Contratos", "Histórico Inadimplência", "Concentração", "Governança", "Garantias"]
        pesos_qualitativas = [20, 20, 15, 15, 15, 15]
        df_all['Score Estrutural'] = df_all[col_qualitativas].dot(np.array(pesos_qualitativas)) * 20 / 100

        # Score final
        wq, we = 0.7, 0.3
        df_all['Score Final'] = wq * df_all['Score Quantitativo'] + we * df_all['Score Estrutural']

        def classificar_nota(score):
            if score >= 90: return 'AAA'
            elif score >= 80: return 'AA'
            elif score >= 70: return 'A'
            elif score >= 60: return 'BBB'
            elif score >= 50: return 'BB'
            elif score >= 40: return 'B'
            elif score >= 30: return 'CCC'
            elif score >= 20: return 'CC'
            elif score >= 10: return 'C'
            else: return 'D'

        df_all['Nota'] = df_all['Score Final'].apply(classificar_nota)

        # Exportar
        df_all.to_csv(ARQ_RESULTADO, sep=';', decimal=',', index=False)

        # Log
        if os.path.exists(ARQ_LOG):
            log_usuarios = pd.read_csv(ARQ_LOG, sep=';', decimal=',')
        else:
            log_usuarios = pd.DataFrame(columns=["Timestamp", "Usuário", "Função", "Ação", "Fundo", "DtReferencia", "Detalhes"])

        for _, row in df_all.iterrows():
            log_usuarios = pd.concat([log_usuarios, pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Usuário": usuario,
                "Função": funcao,
                "Ação": "Cálculo Rating",
                "Fundo": row['NmFundo'],
                "DtReferencia": row['DtReferencia'],
                "Detalhes": f"Nota: {row['Nota']} | Score Final: {row['Score Final']:.2f}"
            }])], ignore_index=True)

        log_usuarios.to_csv(ARQ_LOG, sep=';', decimal=',', index=False)

        st.success("Cálculo realizado com sucesso!")
        st.dataframe(df_all[['NmFundo', 'DtReferencia', 'Tipo', 'Score Final', 'Nota']], use_container_width=True)
else:
    st.warning("⚠️ Faça login preenchendo nome e função na barra lateral para continuar.")
