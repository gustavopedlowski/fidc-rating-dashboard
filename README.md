# 📊 Sistema de Rating Interno – FIDCs (Catálise Investimentos)

Este repositório contém a aplicação de rating interno da Catálise Investimentos para fundos de investimento em direitos creditórios (FIDCs), com base em uma metodologia quantitativa e qualitativa proprietária. O sistema é totalmente modularizado, com controle de login, logs de auditoria e esteira de aprovação para governança regulatória.

---

## 🚀 Funcionalidades Principais

* ✅ Cadastro de notas qualitativas por fundo e mês (score estrutural)
* ✅ Upload de dados operacionais mensais dos FIDCs (score quantitativo)
* ✅ Cálculo do rating interno (score final + nota AAA a D)
* ✅ Sistema de login por usuário e função (com rastreabilidade)
* ✅ Logs automáticos para cada ação executada (auditoria completa)
* ✅ Interface amigável via Streamlit Cloud

---

## 🗂️ Estrutura do Projeto

```
fidc-rating/
├── Home.py                          # Página inicial (explicativa)
├── cadastro_structural_form.py     # Cadastro de notas qualitativas (com login + logs)
├── cadastro_dados_quantitativos.py # Upload de dados operacionais (com login + logs)
├── pages/
│   └── 1_rating_engine.py          # Cálculo do score final e nota (com login + logs)
├── logs/
│   ├── historico_scores_estruturais.csv # Base com notas estruturais por fundo e mês
│   └── atividade_usuarios.csv           # Log de ações por usuário
├── dados_fidcs.csv                # Dados operacionais dos FIDCs (upload manual)
├── requirements.txt               # Dependências da aplicação
└── README.md
```

---

## 📥 Como usar via Streamlit Cloud

1. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/fidc-rating.git
```

2. Acesse [https://streamlit.io/cloud](https://streamlit.io/cloud)

3. Clique em **New App** e selecione:

   * Repositório: `fidc-rating`
   * Branch: `main`
   * Arquivo principal: `Home.py`

4. O menu lateral exibirá:

   * 📝 Cadastro Estrutural
   * 📥 Dados Quantitativos
   * 📊 Rating Final

5. Faça login, execute os fluxos e acompanhe os logs automaticamente.

---

## 🔐 Controle de Login e Logs

Cada módulo inicia com login obrigatório:

* **Nome do usuário**
* **Função** (Riscos, Compliance, Aprovador, etc.)

Cada ação (cadastro, upload, cálculo) gera um log em `logs/atividade_usuarios.csv`, incluindo:

* Timestamp
* Nome e função do usuário
* Fundo e data de referência
* Tipo de ação executada
* Detalhes técnicos (ex: nota atribuída, score final)

---

## 📊 Lógica do Rating

### Score Final:

```latex
\text{Score Final} = 0.7 \cdot \text{Score Quantitativo} + 0.3 \cdot \text{Score Estrutural}
```

### Notas atribuídas:

| Score Final | Nota |
| ----------- | ---- |
| ≥ 90        | AAA  |
| ≥ 80        | AA   |
| ≥ 70        | A    |
| ≥ 60        | BBB  |
| ≥ 50        | BB   |
| ≥ 40        | B    |
| ≥ 30        | CCC  |
| ≥ 20        | CC   |
| ≥ 10        | C    |
| < 10        | D    |

---

## 📎 Requisitos

```
pandas
numpy
scikit-learn
streamlit
```

Instale com:

```bash
pip install -r requirements.txt
```

---

## 👤 Autoria

Sistema desenvolvido por Gustavo Pedlowski

---

## 📄 Licença

Uso interno exclusivo. Direitos reservados à Catálise Investimentos.
