# 🔥 Projeto G1 — Análise de Queimadas no Brasil

**Aluno:** Théo Cubas Reis  
**Tema:** 03 — Análise de Queimadas no Brasil  
**Período:** 2015–2024
**Professor:** Alexandre Neves Louzada

## Objetivo

Investigar a evolução dos focos de queimadas no Brasil, identificando padrões temporais,
regionais, estaduais, por bioma e por nível de risco, além de analisar a relação entre
índice de seca e quantidade de focos.

## Tecnologias

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- SQLAlchemy + SQLite
- GitHub / GitHub Pages / Streamlit Community Cloud

## Estrutura

```text
projeto-queimadas-brasil/
├── app.py
├── requirements.txt
├── README.md
├── index.html
├── dados/
│   └── simulacao_queimadas_brasil.csv
├── database/
│   └── queimadas.db
├── notebooks/
│   └── analise_queimadas.ipynb
└── imagens/
```

## Como executar

```bash
pip install -r requirements.txt
streamlit run app.py
```

O banco SQLite é criado/atualizado automaticamente na primeira execução.

## Funcionalidades

- filtros por ano, mês, região, UF, bioma e risco;
- KPIs dinâmicos;
- evolução temporal;
- sazonalidade;
- comparação entre regiões;
- ranking de estados;
- análise por bioma;
- relação entre seca e queimadas;
- análise de risco;
- tabela dinâmica;
- persistência em SQLite;
- gráficos interativos com Plotly.

## Resultados iniciais da base

A base possui 2.400 registros, 20 UFs, 6 biomas e cobre 2015–2024.
O total da base é de 61.803 focos e 24.874,64 km² de área atingida.
A correlação entre `indice_seca` e `focos_queimada` é aproximadamente 0,815.

## Publicação

Após subir o projeto ao GitHub:

1. Ative o GitHub Pages para publicar `index.html`.
2. No Streamlit Community Cloud, selecione o repositório e o arquivo `app.py`.
3. Substitua os placeholders do `index.html` pelos links reais.

> Os resultados são baseados em uma base simulada fornecida para a disciplina.
