"""
SSF — Consulta Pública de Sustentabilidade Financeira
Painel demonstrativo (Série Rio). Não é ferramenta oficial da CBF/ANRESF.

Como rodar:
    pip install -r requirements.txt
    streamlit run app.py
"""
import streamlit as st
import pandas as pd

# ============================================================
# IDENTIDADE VISUAL (azul institucional + dourado + verde)
# ============================================================
AZUL   = "#0A2A5E"   # azul institucional (base)
AZUL2  = "#143C82"
DOURADO= "#C9A227"   # dourado (ANRESF)
VERDE  = "#0B7A4B"   # verde (CBF/bandeira)
VERMELHO="#B23A3A"
AMARELO= "#E8B600"
CINZA  = "#5A6470"
BG     = "#FFFFFF"

st.set_page_config(page_title="SSF — Consulta de Sustentabilidade Financeira",
                   page_icon="⚖️", layout="wide")

st.markdown(f"""
<style>
.stApp {{ background:{BG}; }}
.block-container {{ padding-top:1.2rem; max-width:1100px; }}
h1,h2,h3 {{ color:{AZUL}; font-family:Arial,sans-serif; }}
.cabecalho {{
  background:linear-gradient(100deg,{AZUL} 0%,{AZUL2} 100%);
  color:#fff; padding:22px 28px; border-radius:14px; margin-bottom:8px;
  border-left:10px solid {DOURADO};
}}
.cabecalho h1 {{ color:#fff!important; margin:0; font-size:30px; }}
.cabecalho p {{ color:#dCe4f2; margin:4px 0 0 0; font-size:15px; }}
.selo {{
  display:inline-block; padding:10px 26px; border-radius:40px;
  font-weight:800; font-size:22px; letter-spacing:.5px; color:#fff;
}}
.req-card {{
  border:1px solid #E2E8F0; border-radius:12px; padding:16px 18px; margin-bottom:6px;
  background:#FCFDFF;
}}
.req-titulo {{ font-weight:700; color:{AZUL}; font-size:17px; margin-bottom:2px; }}
.req-frase {{ color:#33414F; font-size:15px; margin:6px 0; }}
.barra-fundo {{ background:#EAEEF5; border-radius:8px; height:22px; width:100%; position:relative; overflow:hidden; }}
.barra-valor {{ height:22px; border-radius:8px; }}
.lim-marca {{ position:absolute; top:-3px; width:3px; height:28px; background:{AZUL}; }}
.rodape {{ color:{CINZA}; font-size:12px; margin-top:24px; border-top:1px solid #E2E8F0; padding-top:10px; }}
.traj-ok {{ color:{VERDE}; font-weight:800; }}
.traj-x  {{ color:{VERMELHO}; font-weight:800; }}
table.traj {{ border-collapse:collapse; width:100%; }}
table.traj th, table.traj td {{ border:1px solid #DCE3EC; padding:8px 10px; text-align:center; font-size:14px; }}
table.traj th {{ background:{AZUL}; color:#fff; }}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DADOS (R$ mil) — balanços auditados 2023–2025
# Texto AZUL na planilha = inputs; aqui são os dados-fonte.
# ============================================================
ANOS_DADOS = [2023, 2024, 2025]
CLUBES = ["Flamengo", "Fluminense", "Vasco SAF", "Botafogo SAF"]

# cada métrica: {clube: [2023,2024,2025]}
DADOS = {
 "receita":   {"Flamengo":[1012380,1158862,1499741],"Fluminense":[458713,399624,758546],"Vasco SAF":[222091,282340,413878],"Botafogo SAF":[279197,552271,574006]},
 "transf":    {"Flamengo":[303493,107384,518741],"Fluminense":[16106,268169,233378],"Vasco SAF":[127181,170258,123866],"Botafogo SAF":[77000,96356,733361]},
 "folha":     {"Flamengo":[463050,524040,711094],"Fluminense":[257820,371159,521663],"Vasco SAF":[145701,178973,232489],"Botafogo SAF":[260450,440012,438141]},
 "amort":     {"Flamengo":[175729,213621,243716],"Fluminense":[18540,32632,84353],"Vasco SAF":[58879,91932,124676],"Botafogo SAF":[91339,129518,236827]},
 "resop":     {"Flamengo":[291699,46131,350886],"Fluminense":[63786,68772,100370],"Vasco SAF":[-70493,-56590,-126472],"Botafogo SAF":[-18309,-160119,-274066]},
 "divida":    {"Flamengo":[167152,165358,162316],"Fluminense":[425879,423768,507755],"Vasco SAF":[285444,245118,351284],"Botafogo SAF":[524659,367859,457479]},
}

# Limites do glide path por ano-parâmetro de cobrança
CUSTO_LIM = {2026:0.90, 2027:0.80, 2028:0.70, 2029:0.70}
ENDIV_LIM = {2026:0.70, 2027:0.60, 2028:0.50, 2029:0.45}
def lim_deficit(receita):  # déficit tolerado: o maior entre 30 mi e 2,5% da receita
    return -max(30000, 0.025*receita)

def idx_clube(clube):
    return CLUBES.index(clube)

def calcula(receita, transf, folha, amort, resop, divida, ano_param):
    custo = folha + amort
    recrel = receita + transf
    ic = custo/recrel if recrel else 0
    ie = divida/receita if receita else 0
    ld = lim_deficit(receita)
    v_custo = ic <= CUSTO_LIM[ano_param]
    v_equil = resop >= ld
    v_endiv = ie <= ENDIV_LIM[ano_param]
    return {
        "indice_custo":ic, "indice_endiv":ie, "result_op":resop, "lim_deficit":ld,
        "v_custo":v_custo, "v_equil":v_equil, "v_endiv":v_endiv,
        "aprovado": v_custo and v_equil and v_endiv,
    }

def fmt(n): return f"{n:,.0f}".replace(",", ".")

# ============================================================
# CABEÇALHO
# ============================================================
st.markdown(f"""
<div class="cabecalho">
  <h1>⚖️ Sustentabilidade Financeira do seu clube</h1>
  <p>Consulta pública · como o clube se posiciona frente aos requisitos do fair play financeiro brasileiro (SSF)</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CONTROLES NO TOPO (janelas)
# ============================================================
c1, c2, c3 = st.columns(3)
with c1:
    clube = st.selectbox("🏆 Clube", ["— selecione um clube —"] + CLUBES, index=0)
with c2:
    modo = st.selectbox("📅 Base de dados", ["2025 (mais recente)", "2024", "2023", "Projeção (editar)"])
with c3:
    ano_param = st.selectbox("🎯 Cobrança no ano de", [2026, 2027, 2028, 2029], index=0,
                             help="O regulamento aperta os limites a cada ano (glide path). Veja como os mesmos números seriam avaliados em cada ano.")

i = idx_clube(clube) if clube in CLUBES else None

# ============================================================
# VISÃO GERAL — tabela dos quatro clubes (sempre no topo)
# ============================================================
# resolve o ano de dados para a tabela geral
if modo.startswith("2025"): yr_tab=2
elif modo=="2024": yr_tab=1
elif modo=="2023": yr_tab=0
else: yr_tab=2  # na projeção, a tabela geral mostra 2025 real

st.markdown("### Visão geral — os quatro clubes")
st.markdown(f"<div style='color:{CINZA};font-size:14px;margin-bottom:8px;'>"
            f"Situação de cada clube com base em <b>{ANOS_DADOS[yr_tab]}</b>, "
            f"avaliada pelos limites de <b>{ano_param}</b>. Selecione um clube acima para ver a ficha detalhada.</div>",
            unsafe_allow_html=True)

def selo_html(aprovado, n_falhas):
    if aprovado: c,t = VERDE,"APROVADO"
    elif n_falhas==1: c,t = AMARELO,"EM ALERTA"
    else: c,t = VERMELHO,"REPROVADO"
    return f'<span style="background:{c};color:#fff;padding:3px 12px;border-radius:20px;font-weight:700;font-size:13px;">{t}</span>'

def chk(ok): return f'<span style="color:{VERDE};font-weight:800;">✓</span>' if ok else f'<span style="color:{VERMELHO};font-weight:800;">✗</span>'

rows_tab=""
for idx,cl in enumerate(CLUBES):
    rr=calcula(DADOS["receita"][cl][yr_tab],DADOS["transf"][cl][yr_tab],DADOS["folha"][cl][yr_tab],
               DADOS["amort"][cl][yr_tab],DADOS["resop"][cl][yr_tab],DADOS["divida"][cl][yr_tab],ano_param)
    nf=sum([not rr["v_custo"],not rr["v_equil"],not rr["v_endiv"]])
    bg = "#F2F6FC" if idx%2 else "#FFFFFF"
    rows_tab+=(f'<tr style="background:{bg};"><td style="text-align:left;font-weight:600;">{cl}</td>'
               f'<td>{chk(rr["v_equil"])}</td><td>{chk(rr["v_custo"])}</td><td>{chk(rr["v_endiv"])}</td>'
               f'<td>{selo_html(rr["aprovado"],nf)}</td></tr>')
st.markdown(
'<table class="traj"><tr><th style="text-align:left;">Clube</th>'
'<th>Equilíbrio</th><th>Custo elenco</th><th>Endividamento</th><th>Situação</th></tr>'
+ rows_tab + '</table>', unsafe_allow_html=True)

# ============================================================
# A PARTIR DAQUI: ficha individual (só se um clube foi escolhido)
# ============================================================
if i is None:
    st.markdown(f"<div style='margin-top:26px;padding:18px;background:#F7F9FC;border-radius:12px;"
                f"border-left:6px solid {DOURADO};color:{CINZA};font-size:15px;'>"
                "👆 Selecione um clube no menu acima para abrir a ficha detalhada, com medidores por "
                "requisito e a trajetória ano a ano.</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class="rodape">
Painel demonstrativo da série <b>Série Rio</b>. Não é ferramenta oficial da CBF ou da ANRESF.
Dados: balanços auditados de 2023–2025. Régua: Regulamento SSF/CBF 2025 (Equilíbrio, Custo com Elenco e Endividamento).
Valores em R$ mil. Os vereditos são um exercício analítico independente.</div>""", unsafe_allow_html=True)
    st.stop()

st.markdown("---")
st.markdown(f"## Ficha detalhada — {clube}")

# resolve base de dados
if modo.startswith("2025"): yr=2
elif modo=="2024": yr=1
elif modo=="2023": yr=0
else: yr=None  # projeção

if yr is not None:
    receita=DADOS["receita"][clube][yr]; transf=DADOS["transf"][clube][yr]
    folha=DADOS["folha"][clube][yr]; amort=DADOS["amort"][clube][yr]
    resop=DADOS["resop"][clube][yr]; divida=DADOS["divida"][clube][yr]
else:
    st.markdown("##### ✏️ Projeção — ajuste os números e veja o veredito recalcular")
    p1,p2,p3 = st.columns(3)
    base=2  # parte de 2025
    with p1:
        receita=st.number_input("Receita operacional (R$ mil)", value=DADOS["receita"][clube][base], step=10000)
        transf=st.number_input("Receita de transferências (R$ mil)", value=DADOS["transf"][clube][base], step=10000)
    with p2:
        folha=st.number_input("Folha + comissões (R$ mil)", value=DADOS["folha"][clube][base], step=10000)
        amort=st.number_input("Amortização de atletas (R$ mil)", value=DADOS["amort"][clube][base], step=10000)
    with p3:
        resop=st.number_input("Resultado operacional (R$ mil)", value=DADOS["resop"][clube][base], step=10000)
        divida=st.number_input("Dívida total (emprést.+fiscal) (R$ mil)", value=DADOS["divida"][clube][base], step=10000)

R = calcula(receita, transf, folha, amort, resop, divida, ano_param)

# ============================================================
# SELO DE SITUAÇÃO
# ============================================================
n_falhas = sum([not R["v_custo"], not R["v_equil"], not R["v_endiv"]])
if R["aprovado"]:
    cor, txt = VERDE, "APROVADO"
elif n_falhas == 1:
    cor, txt = AMARELO, "EM ALERTA"
else:
    cor, txt = VERMELHO, "REPROVADO"

st.markdown("###")
sc1, sc2 = st.columns([1,2])
with sc1:
    st.markdown(f'<div class="selo" style="background:{cor};">{txt}</div>', unsafe_allow_html=True)
with sc2:
    base_txt = modo if yr is not None else "sua projeção"
    st.markdown(f"<div style='font-size:15px;color:{CINZA};padding-top:8px;'>"
                f"Situação de <b>{clube}</b> com base em <b>{base_txt}</b>, "
                f"avaliado pelos limites de <b>{ano_param}</b>.</div>", unsafe_allow_html=True)

# ============================================================
# OS TRÊS REQUISITOS COM MEDIDOR
# ============================================================
st.markdown("### Os requisitos, um a um")

def barra(valor_pct, limite_pct, ok, inverso=False):
    escala = max(valor_pct, limite_pct, 1.0)*1.15
    largura = min(valor_pct/escala*100, 100)
    pos = min(limite_pct/escala*100, 100)
    cor = VERDE if ok else VERMELHO
    return (f'<div class="barra-fundo"><div class="barra-valor" style="width:{largura:.1f}%; background:{cor};"></div>'
            f'<div class="lim-marca" style="left:{pos:.1f}%;"></div></div>')

# Custo com elenco
ok=R["v_custo"]; lim=CUSTO_LIM[ano_param]
st.markdown(
f'<div class="req-card"><div class="req-titulo">1 · Custo com o elenco</div>'
f'<div class="req-frase">O clube comprometeu <b>{R["indice_custo"]*100:.1f}%</b> da sua receita relevante com o elenco '
f'(salários + amortização de atletas). O limite para {ano_param} é <b>{lim*100:.0f}%</b>. '
f'{"Dentro do limite." if ok else "Acima do limite."}</div>'
f'{barra(R["indice_custo"], lim, ok)}</div>', unsafe_allow_html=True)

# Equilíbrio
ok=R["v_equil"]
st.markdown(
f'<div class="req-card"><div class="req-titulo">2 · Equilíbrio da operação</div>'
f'<div class="req-frase">O resultado da operação foi de <b>R$ {fmt(R["result_op"])} mil</b>. '
f'O déficit máximo tolerado para este clube é <b>R$ {fmt(R["lim_deficit"])} mil</b> '
f'(o maior entre R$ 30 milhões e 2,5% da receita). '
f'{"A operação está equilibrada." if ok else "O déficit ultrapassa o tolerado."}</div></div>',
unsafe_allow_html=True)

# Endividamento
ok=R["v_endiv"]; lim=ENDIV_LIM[ano_param]
st.markdown(
f'<div class="req-card"><div class="req-titulo">3 · Endividamento de curto prazo</div>'
f'<div class="req-frase">As dívidas que vencem rápido representam <b>{R["indice_endiv"]*100:.1f}%</b> da receita. '
f'O limite para {ano_param} é <b>{lim*100:.0f}%</b>. '
f'{"Dentro do limite." if ok else "Acima do limite."}</div>'
f'{barra(R["indice_endiv"], lim, ok)}</div>', unsafe_allow_html=True)

# ============================================================
# TRAJETÓRIA — os mesmos números ao longo do glide path
# ============================================================
st.markdown("### Como esses números se comportam ao longo da régua")
st.markdown(f"<div style='color:{CINZA};font-size:14px;margin-bottom:8px;'>"
            "O regulamento aperta os limites a cada ano. A tabela mostra como <b>estes mesmos números</b> "
            "seriam avaliados em cada ano do calendário — uma característica da régua, não uma recomendação.</div>",
            unsafe_allow_html=True)

def cel(ok): return f'<span class="traj-ok">✓</span>' if ok else f'<span class="traj-x">✗</span>'
linhas=""
reqs=[("Custo com elenco","v_custo"),("Equilíbrio","v_equil"),("Endividamento","v_endiv")]
for nome,chave in reqs:
    cells=""
    for ay in [2026,2027,2028,2029]:
        rr=calcula(receita,transf,folha,amort,resop,divida,ay)
        cells+=f"<td>{cel(rr[chave])}</td>"
    linhas+=f"<tr><td style='text-align:left;font-weight:600;'>{nome}</td>{cells}</tr>"
# linha consolidada
cons=""
for ay in [2026,2027,2028,2029]:
    rr=calcula(receita,transf,folha,amort,resop,divida,ay)
    cons+=f"<td>{cel(rr['aprovado'])}</td>"
linhas+=f"<tr style='background:#F2F6FC;'><td style='text-align:left;font-weight:800;'>Situação geral</td>{cons}</tr>"

st.markdown(
'<table class="traj"><tr><th style="text-align:left;">Requisito</th>'
'<th>2026</th><th>2027</th><th>2028</th><th>2029</th></tr>'
+ linhas + '</table>'
f'<div style="font-size:12px;color:{CINZA};margin-top:6px;">'
'Limites — Custo elenco: 90% / 80% / 70% / 70%. &nbsp; Endividamento: 70% / 60% / 50% / 45%. &nbsp; '
'Equilíbrio: déficit ≤ maior(R$ 30 mi; 2,5% da receita).</div>',
unsafe_allow_html=True)

# ============================================================
# O QUE ISSO SIGNIFICA
# ============================================================
st.markdown("### O que isso significa")
if R["aprovado"]:
    msg = (f"No ano-base escolhido, o {clube} cumpre os três requisitos do SSF para {ano_param}. "
           "Isso indica que o clube opera dentro da capacidade que a régua brasileira considera sustentável: "
           "gasta com elenco em proporção aceitável à receita, não acumula déficit operacional acima do tolerado "
           "e mantém a dívida de curto prazo sob controle.")
else:
    falhou=[]
    if not R["v_custo"]: falhou.append("custo com elenco")
    if not R["v_equil"]: falhou.append("equilíbrio da operação")
    if not R["v_endiv"]: falhou.append("endividamento de curto prazo")
    lista=", ".join(falhou)
    msg = (f"No ano-base escolhido, o {clube} não cumpre {'o requisito de' if len(falhou)==1 else 'os requisitos de'} "
           f"{lista}, frente aos limites de {ano_param}. "
           "Isso não significa punição automática — o regulamento prevê regimes de adaptação e a possibilidade de "
           "cobrir déficits com aporte de capital. Significa que, nesta dimensão, as contas do clube estão fora do "
           "que a régua considera sustentável para o ano avaliado.")
st.markdown(f"<div style='font-size:15px;color:#33414F;line-height:1.6;'>{msg}</div>", unsafe_allow_html=True)

# ============================================================
# RODAPÉ
# ============================================================
st.markdown(f"""
<div class="rodape">
Painel demonstrativo da série <b>Série Rio</b>. Não é ferramenta oficial da CBF ou da ANRESF.
Dados: balanços auditados de 2023–2025. Régua: Regulamento SSF/CBF 2025 (Equilíbrio, Custo com Elenco e Endividamento).
Valores em R$ mil. Os vereditos são um exercício analítico independente.
</div>
""", unsafe_allow_html=True)