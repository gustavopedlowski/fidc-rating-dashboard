# 📊 Dashboard de Rating para FIDCs

Este projeto é um painel interativo construído em **Streamlit** para calcular e visualizar o rating de **FIDCs (Fundos de Investimento em Direitos Creditórios)** com base em métricas operacionais e de risco.

## 🚀 Acesse o app online

Você pode acessar o dashboard publicado aqui:

👉 [https://gustavopedlowski.streamlit.app/](https://gustavopedlowski.streamlit.app/)

---

## 🧠 O que o dashboard faz?

Com base em um arquivo `.csv` contendo indicadores mensais dos FIDCs, o painel realiza:

- **Análise estatística com PCA (Principal Component Analysis)**
- **Cálculo de Score de Risco por fundo**
- **Visualização dos fundos mais saudáveis e mais arriscados**
- **Gráficos interativos de distribuição de score e importância de métricas**

---

## 📁 Como usar

1. Prepare um arquivo `.csv` com as métricas por fundo (ver abaixo)
2. Acesse o app no Streamlit
3. Faça upload do arquivo
4. Visualize os resultados diretamente no navegador!

---

## 📄 Formato esperado do arquivo `.csv`

O arquivo deve conter as colunas (nomes exatos):

- `NmFundo`
- `DtReferencia`
- `A Vencer / PL (Presente)`
- `Vencidos / PL (Presente)`
- `PDD / PL`
- `Prazo Médio Ponderado`
- `Qtd Cedentes Fim de Mes`
- `Qtd Sacados Fim de Mes`
- `Quantidade de Titulos`
- `Valor Medio dos Titulos`
- `Indice de Subordinacao`
- `Rentabilidade Patrimonio Mensal`
- `DesvioPadraoPorData`

---

## ⚙️ Requisitos

- Python 3.8 ou superior
- Bibliotecas:
  ```txt
  streamlit
  pandas
  numpy
  scikit-learn
  matplotlib
  seaborn
