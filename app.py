import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Queimadas no Brasil",
    page_icon="🔥",
    layout="wide"
)

DATA_PATH = "dados/simulacao_queimadas_brasil.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["data"])
    df["ano"] = df["ano"].astype(int)
    df["mes"] = df["mes"].astype(int)
    return df

def mes_nome(m):
    nomes = [
        "Janeiro", "Fevereiro", "Março", "Abril",
        "Maio", "Junho", "Julho", "Agosto",
        "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    return nomes[int(m) - 1]

df = load_data()

st.title("🔥 Análise de Queimadas no Brasil")

st.markdown("""
**Projeto G1 — Théo Cubas Reis | Alexandre Neves Louzada | Tema 03**

Este dashboard investiga a evolução dos focos de queimadas no Brasil entre 2015 e 2024,
com foco em padrões temporais, diferenças regionais, biomas, estados, risco ambiental
e relação entre estiagem e ocorrências.
""")

with st.sidebar:
    st.header("Filtros")

    anos = st.multiselect(
        "Ano",
        sorted(df["ano"].unique()),
        default=sorted(df["ano"].unique())
    )

    meses = st.multiselect(
        "Mês",
        list(range(1, 13)),
        default=list(range(1, 13)),
        format_func=mes_nome
    )

    regioes = st.multiselect(
        "Região",
        sorted(df["regiao"].unique()),
        default=sorted(df["regiao"].unique())
    )

    ufs = st.multiselect(
        "Estado (UF)",
        sorted(df["uf"].unique()),
        default=sorted(df["uf"].unique())
    )

    biomas = st.multiselect(
        "Bioma",
        sorted(df["bioma"].unique()),
        default=sorted(df["bioma"].unique())
    )

    riscos = st.multiselect(
        "Nível de risco",
        sorted(df["nivel_risco"].unique()),
        default=sorted(df["nivel_risco"].unique())
    )

f = df[
    df["ano"].isin(anos)
    & df["mes"].isin(meses)
    & df["regiao"].isin(regioes)
    & df["uf"].isin(ufs)
    & df["bioma"].isin(biomas)
    & df["nivel_risco"].isin(riscos)
].copy()

if f.empty:
    st.warning("Nenhum registro atende aos filtros selecionados.")
    st.stop()

total_focos = int(f["focos_queimada"].sum())

area_total = f["area_atingida_km2"].sum()

estado = (
    f.groupby("uf")["focos_queimada"]
    .sum()
    .idxmax()
)

regiao = (
    f.groupby("regiao")["focos_queimada"]
    .sum()
    .idxmax()
)

mes = (
    f.groupby("mes")["focos_queimada"]
    .sum()
    .idxmax()
)

media_anual = (
    f.groupby("ano")["focos_queimada"]
    .sum()
    .mean()
)

corr = f["indice_seca"].corr(f["focos_queimada"])

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric(
    "Total de focos",
    f"{total_focos:,}".replace(",", ".")
)

c2.metric(
    "Área atingida",
    f"{area_total:,.2f} km²"
    .replace(",", "X")
    .replace(".", ",")
    .replace("X", ".")
)

c3.metric(
    "Estado mais afetado",
    estado
)

c4.metric(
    "Região mais crítica",
    regiao
)

c5.metric(
    "Mês mais crítico",
    mes_nome(mes)
)

c6.metric(
    "Média anual",
    f"{media_anual:,.0f}".replace(",", ".")
)

st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Evolução temporal",
    "🗺️ Comparações",
    "☀️ Seca e risco",
    "📋 Tabela"
])

with tab1:
    st.subheader("Evolução dos focos de queimadas")

    temporal = (
        f.groupby("ano", as_index=False)
        ["focos_queimada"]
        .sum()
    )

    fig = px.line(
        temporal,
        x="ano",
        y="focos_queimada",
        markers=True,
        labels={
            "ano": "Ano",
            "focos_queimada": "Focos"
        },
        title="Focos de queimadas por ano"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    mensal = (
        f.groupby("mes", as_index=False)
        ["focos_queimada"]
        .sum()
    )

    mensal["mes_nome"] = mensal["mes"].map(mes_nome)

    fig2 = px.bar(
        mensal,
        x="mes_nome",
        y="focos_queimada",
        labels={
            "mes_nome": "Mês",
            "focos_queimada": "Focos"
        },
        title="Sazonalidade dos focos"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        reg = (
            f.groupby("regiao", as_index=False)
            ["focos_queimada"]
            .sum()
            .sort_values(
                "focos_queimada",
                ascending=False
            )
        )

        fig = px.bar(
            reg,
            x="regiao",
            y="focos_queimada",
            text_auto=True,
            title="Focos por região",
            labels={
                "regiao": "Região",
                "focos_queimada": "Focos"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:
        uf = (
            f.groupby("uf", as_index=False)
            ["focos_queimada"]
            .sum()
            .sort_values(
                "focos_queimada",
                ascending=True
            )
        )

        fig = px.bar(
            uf,
            x="focos_queimada",
            y="uf",
            orientation="h",
            text_auto=True,
            title="Ranking dos estados",
            labels={
                "uf": "UF",
                "focos_queimada": "Focos"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    bi = (
        f.groupby("bioma", as_index=False)
        ["focos_queimada"]
        .sum()
        .sort_values(
            "focos_queimada",
            ascending=False
        )
    )

    fig = px.bar(
        bi,
        x="bioma",
        y="focos_queimada",
        text_auto=True,
        title="Focos por bioma",
        labels={
            "bioma": "Bioma",
            "focos_queimada": "Focos"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with tab3:
    col1, col2 = st.columns(2)

    with col1:
        fig = px.scatter(
            f,
            x="indice_seca",
            y="focos_queimada",
            size="area_atingida_km2",
            color="nivel_risco",
            hover_data=[
                "ano",
                "mes",
                "uf",
                "bioma"
            ],
            trendline="ols",
            title=f"Índice de seca × focos (correlação: {corr:.3f})",
            labels={
                "indice_seca": "Índice de seca",
                "focos_queimada": "Focos"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:
        risco = (
            f.groupby(
                "nivel_risco",
                as_index=False
            )["focos_queimada"]
            .sum()
        )

        ordem = [
            "Baixo",
            "Médio",
            "Alto",
            "Crítico"
        ]

        risco["ordem"] = (
            risco["nivel_risco"]
            .map({
                x: i
                for i, x in enumerate(ordem)
            })
        )

        risco = risco.sort_values("ordem")

        fig = px.bar(
            risco,
            x="nivel_risco",
            y="focos_queimada",
            title="Focos por nível de risco",
            labels={
                "nivel_risco": "Risco",
                "focos_queimada": "Focos"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.info(
        f"**Interpretação:** nos dados filtrados, a correlação entre o índice de seca "
        f"e o número de focos é **{corr:.3f}**. Isso indica uma associação positiva "
        f"forte: registros com maior estiagem tendem a apresentar mais focos. "
        f"Correlação não implica causalidade."
    )

with tab4:
    tabela = (
        f.groupby(
            [
                "ano",
                "mes",
                "regiao",
                "uf",
                "bioma",
                "nivel_risco"
            ],
            as_index=False
        )
        .agg(
            focos_queimada=("focos_queimada", "sum"),
            area_atingida_km2=("area_atingida_km2", "sum"),
            temperatura_media=("temperatura_media", "mean"),
            chuva_mm=("chuva_mm", "mean"),
            indice_seca=("indice_seca", "mean"),
            qualidade_ar=("qualidade_ar", "mean")
        )
    )

    st.dataframe(
        tabela,
        use_container_width=True,
        hide_index=True
    )

st.divider()

st.subheader("Conclusão executiva")

st.markdown(
    f"""
No recorte atual, foram contabilizados **{total_focos:,} focos**
e **{area_total:,.2f} km²** de área atingida.

O estado com maior volume é **{estado}**, enquanto a região
com maior concentração é **{regiao}**. O mês mais crítico é
**{mes_nome(mes)}**.

A análise de seca apresenta correlação de **{corr:.3f}** com os focos.
Esse resultado reforça a importância de acompanhar indicadores climáticos
e períodos de estiagem na identificação de áreas e períodos de maior risco.

Os resultados devem ser interpretados como padrões observados na
**base simulada**, e não como estimativas oficiais de queimadas no Brasil.
"""
)

st.caption(
    "Projeto G1 — Théo Cubas Reis | Dados simulados fornecidos para a disciplina."
)
