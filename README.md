# 📊 Data Pipeline Didático

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://data-pipeline-learn.streamlit.app)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=flat&logo=github)](https://github.com/HilarioGouveia-Academicos/data-pipeline-learn)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/hilariogouveia/)

Um ambiente interativo e didático construído com **Streamlit** para o ensino e aprendizagem prática dos fundamentos de **Engenharia de Dados**, **Análise Exploratória** e preparação para **Machine Learning**.

O projeto ilustra o ciclo de vida completo de um pipeline de dados adotando uma versão simplificada da **Arquitetura Medallion** (*Bronze ➔ Silver ➔ Gold*), permitindo aos alunos auditar em tempo real a evolução física e analítica dos dados.

🌐 **Acesse a aplicação em produção:** [data-pipeline-learn.streamlit.app](https://data-pipeline-learn.streamlit.app)

---

## 🎯 Objetivo Pedagógico

O principal propósito desta aplicação é demonstrar na prática:

1. **Rastreabilidade e Linhagem de Dados (Data Lineage):** Persistência física em disco de cada camada do pipeline.
2. **Avaliação de Qualidade (Data Quality Gate):** Diagnóstico inicial da camada bruta via *Profiling*.
3. **Auditoria de Transformação:** Métricas de variação volumétrica (perda/ganho de linhas e nulos) e comparativo de tipos (*Schema Diff*).
4. **Enriquecimento para Modelagem:** Engenharia de atributos (*Discretização* e *One-Hot Encoding*).
5. **Consumo e Exploração Visual:** Análise multidimensional livre com interface interativa.

---

## 🏗️ Arquitetura do Pipeline

O fluxo de dados segue a estrutura clássica de data lakes e pipelines modernos:

[Upload CSV]
     │
     ▼

```
┌───────────────┐
│ 01_raw        │ ➔ 📦 1. Ingestão & Profiling (Bronze)
│ (Dados Brutos)│    - Amostragem, auditoria de volumetria e laudo diagnóstico.
└───────┬───────┘
│ (Deduplicação & Imputação)
▼
┌───────────────┐
│ 02_silver     │ ➔ 🧹 2. Limpeza & Tratamento (Silver)
│ (Dados Limpos)│    - Remoção de duplicatas, tratamento de nulos e schema diff.
└───────┬───────┘
│ (Feature Engineering & Bins)
▼
┌───────────────┐
│ 03_gold       │ ➔ 🔧 3. Engenharia de Features (Gold)
│ (Tabela Final)│    - Criação de variáveis dummies e intervalos numéricos.
└───────┬───────┘
│
▼
┌───────────────┐
│ Análise / ML  │ ➔ 📊 4. Visualização Interativa (PyGWalker)
│               │    - Exploração livre com canvas estilo Tableau/PowerBI.
└───────────────┘
```

---

## 🚀 Funcionalidades

- **Entrada de Dados Fixa no Topo:** Upload de CSV diretamente no topo da barra lateral, com crachá (*badge*) do arquivo ativo e modo retrátil para evitar poluição visual.
- **Camada Bronze (Ingestão & Profiling):**
  - Métricas imediatas de integridade (linhas, colunas, nulos e duplicatas).
  - Diagnóstico automatizado sob demanda com **YData-Profiling** (com cache inteligente).
- **Camada Silver (Limpeza Interativa):**
  - Remoção opcional de registros duplicados.
  - Imputação de valores nulos (mediana para numéricos e moda para categóricos).
  - Auditoria volumétrica em tempo real com deltas de linhas e nulos eliminados.
- **Camada Gold (Feature Engineering):**
  - Discretização de variáveis contínuas em intervalos (*bins*).
  - Codificação de variáveis categóricas via *One-Hot Encoding*.
  - Auditoria de mutação de atributos com indicação de novas features.
- **Data Viz Multidimensional:**
  - Exploração comparativa selecionando qualquer camada do pipeline (`01_raw`, `02_silver` ou `03_gold`) com **PyGWalker**.
- **Exportação dos Artefatos:** Botão de download direto (`.csv`) em cada fase do ciclo.

---

## 📚 Manuais e Documentação Complementar

Para aprofundar o uso das ferramentas analíticas integradas, consulte os manuais práticos ilustrados:

- 📑 [**Manual do Usuário: YData-Profiling**](docs/manual-ydataprofiling.md) – Guia completo de interpretação dos relatórios estatísticos, correlações e matrizes de dados faltantes.
- 📊 [**Manual do Usuário: PyGWalker**](docs/manual-pygwalker.md) – Instruções práticas passo a passo para construção de gráficos interativos arrastando e soltando dimensões e medidas.

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.10+](https://www.python.org/)
- [Streamlit](https://streamlit.io/) – Interface web e gerenciamento de estado.
- [Pandas](https://pandas.pydata.org/) – Manipulação e transformação tabular.
- [YData-Profiling](https://github.com/ydataai/ydata-profiling) – Geração de laudos estatísticos automatizados.
- [PyGWalker](https://github.com/Kanaries/pygwalker) – Visualizador analítico multidimensional integrado.

---

## 📂 Estrutura do Projeto

O projeto é modularizado de forma a desacoplar a lógica de negócio das páginas de apresentação:

```text
data-pipeline-learn/
├── data/
│   ├── 01_raw/                 # Arquivos originais imutáveis
│   ├── 02_silver/              # Dados tratados e limpos
│   └── 03_gold/                # Tabelas analíticas com features prontas
├── docs/
│   ├── manual-ydataprofiling.md # Manual prático de EDA com YData-Profiling
│   ├── manual-pygwalker.md      # Manual de exploração visual com PyGWalker
│   └── images/                 # Prévias visuais e capturas de tela
├── src/
│   ├── __init__.py
│   ├── pipeline_ops.py         # Funções puras de transformação, imputação e schemas
│   ├── ui_components.py        # Componentes de UI (upload no topo, CSS e downloads)
│   └── pages/
│       ├── __init__.py
│       ├── p01_ingestion.py    # 1. Ingestão & Profiling (Bronze)
│       ├── p02_cleaning.py     # 2. Limpeza e Qualificação (Silver)
│       ├── p03_wrangling.py    # 3. Engenharia de Features (Gold)
│       └── p04_viz.py          # 4. Exploração Visual Multidimensional (Viz)
├── app.py                      # Ponto de entrada (entrypoint) e orquestração de navegação
├── requirements.txt            # Dependências do projeto
└── README.md                   # Documentação principal
```

---

## ▶️ Como Executar Localmente

### 1. Clonar o Repositório

```bash
git clone [https://github.com/HilarioGouveia-Academicos/data-pipeline-learn.git](https://github.com/HilarioGouveia-Academicos/data-pipeline-learn.git)
cd data-pipeline-learn
```

### 2. Criar e Ativar o Ambiente Virtual

No Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No Windows (PowerShell / Prompt):

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 4. Inicializar a Aplicação

```bash
streamlit run app.py
```

---

## 📖 Roteiro Didático Sugerido para Aulas

1. **Upload do Dataset:** Utilize um arquivo de treino clássico (e.g., Titanic, Churn ou Varejo).
2. **Inspeção na Camada Bronze:** Observe a contagem de nulos e gere o laudo do *YData-Profiling* para identificar colunas críticas.
3. **Tratamento na Camada Silver:** Selecione as colunas para imputação, decida se deve remover duplicatas e observe as métricas de impacto volumétrico e o comparativo de schema.
4. **Construção da Camada Gold:** Discretize variáveis numéricas e crie variáveis *dummy* para demonstrar a preparação prévia para modelos de Machine Learning.
5. **Exploração Visual:** Alterne entre `01_raw` e `03_gold` no PyGWalker para que os alunos vejam visualmente o benefício dos dados higienizados e das novas features.

---

## 👤 Autor

Desenvolvido por **Hilário Gouveia**

* 💼 **LinkedIn:** [linkedin.com/in/hilário-gouveia-30a09b26b](https://www.linkedin.com/in/hilário-gouveia-30a09b26b)

* 🐙 **GitHub:** [github.com/HilarioGouveia](https://github.com/HilarioGouveia)

---

## 📜 Licença

Projeto desenvolvido para fins educacionais e didáticos, aberto para uso, modificação e extensão em sala de aula.
