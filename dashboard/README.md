# 📊 Dashboard — Consulta de Sustentabilidade Financeira (SSF)

Painel interativo que mostra como cada clube se posiciona frente aos três requisitos do **fair play financeiro brasileiro (SSF / CBF)**: equilíbrio da operação, custo com elenco e endividamento de curto prazo.

É a "consulta pública" imaginada da série *Série Rio* — pensada como seria um relatório simples, em que qualquer pessoa pudesse abrir e entender a situação do próprio clube. **Não é ferramenta oficial** da CBF ou da ANRESF.

---

## 🚀 Como rodar

Pré-requisito: **Python 3.9+** instalado.

```bash
# a partir desta pasta (dashboard/)
pip install -r requirements.txt
streamlit run app.py
```

O painel abre sozinho no navegador, geralmente em `http://localhost:8501`.
Para encerrar, pressione `Ctrl + C` no terminal.

> **No Windows**, se `streamlit` não for reconhecido, rode com:
> ```bash
> python -m streamlit run app.py
> ```

---

## 🎛️ Como usar

O painel tem **três controles no topo**:

| Controle | O que faz |
|---|---|
| 🏆 **Clube** | Escolhe o clube. Começa em branco — selecione um para abrir a ficha detalhada. |
| 📅 **Base de dados** | Usa os números reais de **2023, 2024 ou 2025**, ou o modo **Projeção** (você edita os valores). |
| 🎯 **Cobrança no ano de** | Define contra quais limites do *glide path* (2026–2029) os números são avaliados. |

A **visão geral** com os quatro clubes fica sempre no topo. Ao escolher um clube, abre abaixo a **ficha detalhada**: selo de situação, medidores por requisito, a matriz de trajetória ano a ano e a leitura "o que isso significa".

### Modo Projeção

No modo Projeção, você edita os campos básicos (receita, transferências, folha + amortização, resultado operacional e dívida) e o veredito recalcula na hora — útil para simular cenários ("e se o clube abatesse X de dívida?").

---

## ⚖️ Os três requisitos

| Requisito | Cálculo | Limite (glide path) |
|---|---|---|
| **Equilíbrio** | resultado da operação vs. déficit tolerado | déficit ≤ maior(R$ 30 mi; 2,5% da receita) |
| **Custo com elenco** | (folha + amortização) ÷ receita relevante | 90% → 80% → 70% → 70% |
| **Endividamento** | dívida de curto prazo ÷ receita | 70% → 60% → 50% → 45% |

*(Limites na ordem 2026 → 2027 → 2028 → 2029.)*
Receita relevante = receita operacional + transferências + contribuições patrimoniais.

---

## 📁 Arquivos desta pasta

```
dashboard/
├── app.py             # o aplicativo Streamlit
├── requirements.txt   # dependências (streamlit, pandas)
└── README.md          # este arquivo
```

Os dados (balanços auditados 2023–2025) estão embutidos no `app.py`, no dicionário `DADOS` — para atualizar números ou adicionar clubes, basta editar esse bloco.

---

## ⚠️ Limitações

- O **endividamento** usa um perímetro homogêneo (empréstimos + parcelamentos fiscais) como aproximação do OLCP, para permitir comparação entre os quatro balanços.
- O **equilíbrio** é fiel ao resultado operacional reportado, que pode embutir efeitos não-recorrentes (deságios de recuperação judicial, vendas atípicas de atletas).

---

## 📚 Fontes

- **Dados:** balanços auditados de Flamengo, Fluminense, Vasco SAF e Botafogo SAF (2023–2025).
- **Régua:** Regulamento SSF/CBF 2025 (Seções 3, 4 e 5).

Valores em R$ mil. Exercício analítico independente — não é relatório oficial.

---

↩️ Voltar ao [repositório principal](../README.md)
