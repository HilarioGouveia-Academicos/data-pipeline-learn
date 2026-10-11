# 📊 Data Pipeline Didático

Um aplicativo interativo em **Streamlit** que demonstra um pipeline completo de análise de dados:

1. **Data Profiling** com YData-Profiling  
2. **Data Cleaning** interativo  
3. **Data Wrangling** (discretização e encoding)  
4. **Data Visualization** com PyGWalker  

---

## 🚀 Funcionalidades

- Upload de datasets CSV diretamente pela **sidebar**.  
- Relatórios automáticos de **análise exploratória (EDA)** com YData-Profiling.  
- Limpeza interativa:
  - Imputação de valores numéricos (mediana).  
  - Imputação de valores categóricos (moda).  
  - Remoção opcional de duplicados via checkbox.  
- Wrangling:
  - Discretização de variáveis numéricas em faixas.  
  - One-Hot Encoding de variáveis categóricas.  
- Visualização interativa com PyGWalker.  
- Navegação entre páginas usando `st.Page` e `st.navigation`.

---

## 🛠️ Tecnologias

- [Streamlit](https://streamlit.io/) – Interface interativa.  
- [Pandas](https://pandas.pydata.org/) – Manipulação de dados.  
- [YData-Profiling](https://github.com/ydataai/ydata-profiling) – Relatórios de EDA.  
- [PyGWalker](https://github.com/Kanaries/pygwalker) – Visualização interativa.  

---

## 📂 Estrutura do Projeto

```
data-pipeline-learn/
│
├── app.py                # Código principal do Streamlit
├── requirements.txt      # Dependências do projeto
└── README.md             # Documentação
```

---

## ▶️ Como executar

1. Clone o repositório:

   ```bash
   git clone https://github.com/HilarioGouveia-Academicos/data-pipeline-learn.git
   cd data-pipeline-learn
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate      # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute o Streamlit:

   ```bash
   streamlit run app.py
   ```

---

## 📖 Uso

- Faça upload de um arquivo CSV na **sidebar**.  
- Navegue pelas páginas do pipeline:
  - 📦 **Dataset** – Visualização inicial.  
  - 📑 **Data Profiling** – Relatório automático com YData-Profiling.  
  - 🧹 **Data Cleaning** – Imputação e remoção opcional de duplicados.  
  - 🔧 **Data Wrangling** – Discretização e One-Hot Encoding.  
  - 📊 **Data Viz** – Visualização interativa com PyGWalker.  

---

## 🖼️ Exemplos Visuais

### Relatório YData-Profiling

`https://copilot.microsoft.com/th/id/BCO.a6d5900d-9984-4261-acb5-6156d396e5d9.png`

### Visualização PyGWalker

`https://copilot.microsoft.com/th/id/BCO.b95e6523-e4a6-4655-b54e-2d9049bd75ba.png`

---

## 💡 Dicas

- Comece com datasets pequenos (Titanic, Iris).  
- Use o checkbox de duplicados para controlar a limpeza.  
- Experimente diferentes discretizações e encodings para ver o impacto.  
- Combine o relatório do YData-Profiling com as visualizações do PyGWalker para insights mais completos.  

---

## 📜 Licença

Este projeto é didático e pode ser usado livremente para estudo e demonstração.
```
