import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Arquivos de entrada
ARQUIVO_OPERACIONAL = "dados_fidcs.csv"
ARQUIVO_ESTRUTURAL = "historico_scores_estruturais.csv"

# Leitura dos dados
operacional = pd.read_csv(ARQUIVO_OPERACIONAL, sep=';', decimal=',')
estrutural = pd.read_csv(ARQUIVO_ESTRUTURAL, sep=';', decimal=',')

# Pré-processamento
col_id = ["NmFundo", "DtReferencia", "Tipo"]
df_id = operacional[col_id]
df_data = operacional.drop(columns=col_id, errors="ignore")

imputer = SimpleImputer(strategy='median')
df_data = pd.DataFrame(imputer.fit_transform(df_data), columns=df_data.columns)
scaler = StandardScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df_data), columns=df_data.columns)

df_all = pd.concat([df_id.reset_index(drop=True), df_scaled], axis=1)

# Pesos por tipo de fundo
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

# Combinar com score estrutural
df_all = df_all.merge(estrutural, on=["NmFundo", "DtReferencia"], how="left")

col_qualitativas = ["Qualidade Originador", "Contratos", "Histórico Inadimplência", "Concentração", "Governança", "Garantias"]
pesos_qualitativas = [20, 20, 15, 15, 15, 15]

df_all['Score Estrutural'] = df_all[col_qualitativas].dot(np.array(pesos_qualitativas))
df_all['Score Estrutural'] = df_all['Score Estrutural'] * 20 / 100

# Score final e nota
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

# Exportar resultado
df_all.to_csv("Rating_Interno_FIDCs_Resultados.csv", sep=';', decimal=',', index=False)
print("Arquivo 'Rating_Interno_FIDCs_Resultados.csv' gerado com sucesso.")
