# Série Rio — Fair Play Financeiro 🇧🇷⚖️

**Comparação do fair play financeiro brasileiro (SSF) com as cinco maiores ligas da Europa, aplicada aos quatro grandes do Rio de Janeiro.**

Este repositório reúne uma investigação que parte de uma afirmação da CBF sobre o novo **Sistema de Sustentabilidade Financeira (SSF)**:

> *"O modelo apresentado se inspira em regulamentos implementados nas cinco maiores ligas do mundo: Inglaterra, Espanha, Itália, Alemanha e França, mas adapta o que funciona nos países europeus à realidade financeira dos clubes e às particularidades do futebol nacional."*

A pergunta que guia o trabalho: **se o SSF se inspirou nessas cinco ligas, o veredito que ele dá a um clube coincide com o que essas ligas dariam?** Para responder, apliquei as seis réguas (o SSF e as cinco ligas) aos balanços auditados de **Flamengo, Fluminense, Vasco SAF e Botafogo SAF**, no exercício de 2025.

---

## 🔎 O que você encontra aqui

| Item | Descrição |
|---|---|
| 📊 **Dashboard interativo** | Painel em Streamlit que cruza cada clube com os parâmetros do SSF. Escolha o clube, o ano e o ano de cobrança; simule projeções e veja o veredito recalcular. |
| 📈 **Planilha de cálculos** | Workbook auditável e dirigido por fórmulas: altere um número e todos os vereditos recalculam. Uma aba por régua + síntese. |
| 📄 **Comparativo das seis réguas** | Documento com a citação oficial de cada regulamento, a tabela por clube e a avaliação. |
| 📝 **Análise completa** | O texto-investigação que narra a metodologia e os achados de ponta a ponta. |

---

## 🚀 Rodando o dashboard

```bash
# clone o repositório
git clone https://github.com/Vborges95/serie-rio-fairplay.git
cd serie-rio-fairplay/dashboard

# instale as dependências
pip install -r requirements.txt

# rode
streamlit run app.py
```

O painel abre no navegador (geralmente em `http://localhost:8501`). Escolha um clube no menu para abrir a ficha detalhada — com medidores por requisito e a trajetória ano a ano até 2029.

---

## ⚖️ As seis réguas

| Liga | Régua | O que mede |
|---|---|---|
| **Brasil** | SSF / ANRESF | Equilíbrio da operação, custo com elenco e endividamento de curto prazo (limites apertam até 2029). |
| **Inglaterra** | PSR | Perda acumulada em três anos (teto de £105M; só £15M "do próprio dinheiro"). |
| **Espanha** | LCPD | Teto de gasto com elenco = receita − dívida. |
| **Itália** | FIGC | Três indicadores: liquidez, endividamento e custo do trabalho ampliado. |
| **Alemanha** | DFL | Licenciamento por liquidez e patrimônio. |
| **França** | DNCG | Resultado da operação corrente sem transferências (*hors mutation*). |

---

## 🧭 Metodologia

A investigação segue três princípios:

1. **Fórmula nativa.** Cada liga é aplicada com a sua própria definição, a partir do texto oficial do regulamento — não uma versão adaptada.
2. **Fonte primária.** Cada regra vem do documento oficial da entidade. Cada número vem dos balanços auditados.
3. **Limitações declaradas.** Onde a fórmula europeia exige um dado que os balanços brasileiros não segregam, usa-se a aproximação mais fiel possível e a limitação é registrada.

### Classificação de evidências

Ao longo do material, as afirmações são marcadas por nível de evidência:

- 🟢 **documentado** — fonte primária nomeada (balanço auditado ou regulamento oficial)
- 🟡 **inferência forte** — dedução de baixo risco a partir de dado documentado
- 🔵 **leitura analítica** — interpretação própria, não atribuível a uma fonte

---

## 📌 Principais achados

- **Flamengo** passa nas seis réguas — sustentável sob qualquer ótica.
- **Vasco** e **Botafogo** reprovam nas seis — fragilidade estrutural que aparece em qualquer dimensão.
- **Fluminense** é a divergência: aprovado por Brasil (2026) e Inglaterra, reprovado por Espanha, Itália, Alemanha e França. Das cinco ligas que a CBF citou, quatro o reprovariam.

A leitura: o SSF é rigoroso no indicador mais visível (custo com elenco, onde todos passam) e mais suave nas dimensões em que os clubes brasileiros mais sofreriam — liquidez e patrimônio, justamente as que mais reprovam nas réguas europeias. A régua brasileira não é frouxa de forma permanente: ela aperta ano a ano até 2029.

---

## 📚 Fontes oficiais dos regulamentos

- **Brasil — SSF/CBF:** Regulamento do Sistema de Sustentabilidade Financeira (CBF, 2025)
- **Inglaterra — PSR:** Premier League Handbook, Section E
- **Espanha — LCPD:** LaLiga, Normas de Elaboración de Presupuestos
- **Itália — FIGC:** Norme Organizzative Interne, Titolo VI art. 85
- **Alemanha — DFL:** Licensing Regulations (Lizenzierungsordnung)
- **França — DNCG:** Code du sport / Règlement DNCG

Dados: balanços auditados de Flamengo, Fluminense, Vasco SAF e Botafogo SAF (2023–2025). Valores em R$ mil.

---

## 🔗 Série Rio

Este repositório é um spin-off da **Série Rio**, uma análise forense dos balanços auditados dos quatro grandes do Rio de Janeiro. Para ver os outros trabalhos da série — os raios-X financeiros clube a clube, os relatórios e as demais análises:

👉 **[Repositório da Série Rio](https://github.com/Vborges95/serie_rio)**

---

## ⚠️ Aviso

Este é um **exercício analítico independente**, parte da série *Série Rio*. **Não é relatório oficial** da CBF, da ANRESF ou de qualquer entidade. As réguas europeias foram aplicadas em versões adaptadas à realidade contábil brasileira, com as limitações declaradas em cada ponto.

---

*Feito com balanços públicos, regulamentos oficiais e muita planilha.*
