# SER-Standardizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

**Uma ferramenta para padronização de datasets de Reconhecimento de Emoção na Fala (SER).**

O **SER-Standardizer** é um pacote Python desenvolvido para unificar o formato de metadados e áudios de diferentes bancos de dados de emoção na fala. O objetivo principal é facilitar o treinamento cruzado (*cross-corpus training*) e testes de generalização de modelos de aprendizado de máquina, removendo a barreira de pré-processamento manual de cada dataset.

## 📋 Datasets Suportados Atualmente

A ferramenta atualmente suporta o carregamento e padronização dos seguintes bancos de dados:

* **CREMA-D**: Crowd-sourced Emotional Multimodal Actors Dataset.
* **IEMOCAP**: Interactive Emotional Dyadic Motion Capture Database.
* **SAVEE**: Surrey Audio-Visual Expressed Emotion.
* **EmoUERJ**: Banco de dados de emoções em português (Brasil).
* **MSP-IMPROV**: The MSP-Improv Audio-Visual Database.
* **RAVDESS**: The Ryerson Audio-Visual Database of Emotional Speech and Song 

## 🚀 Instalação

### Pré-requisitos
* Python 3.8 ou superior
* Bibliotecas listadas no `pyproject.toml` (instaladas automaticamente).

### Instalação via código fonte

Clone este repositório e instale utilizando o `pip`:

```bash
git clone https://github.com/ViniciusSuaiden/ser-standardizer.git
cd ser-standardizer
pip install .
```

### 💻 Como Usar
O fluxo de trabalho consiste em duas etapas: Pré-processamento (via terminal) e Manipulação dos Dados (via Python).

**1. Pré-processamento (CLI)**

Após a instalação, o comando ser-std estará disponível no seu terminal.
Para padronizar um dataset específico:
```bash
# Exemplo: crema_d
ser-std --dataset crema_d --input_dir /caminho/para/crema
```
O arquivo `.csv` padronizado é inserido na pasta base do usuário, com nomes específicos para cada banco de dados.

**2. API Python**

Após o pré-processamento, utilize a biblioteca para carregar, filtrar e manipular os áudios diretamente em seu código ou Jupyter Notebook.
```python
import ser_standardizer as ser

# Carregar múltiplos datasets em um DataFrame
df_all = ser.load_datasets(["crema_d", "ravdess", "iemocap"])

# Filtrar por dataset, emoção, gênero, língua
df_filtered = ser.filters(
    df_all,
    datasets='ravdess',
    emotions=['anger', 'happy'], 
    genders=['female'],
)

# Toca o áudio localizado no índice 42 do DataFrame
ser.listen(df_filtered, index=42)

# Carrega numpy do índice 0 ao 32
batch_x = ser.load_batch(df_filtered, begin=0, end=32) # Shape ex: (32, 85000)
```

### ✍️ Autores
Vinicius Suaiden - USP - vinicius.suaiden@usp.br

Miguel Arjona Ramirez - USP - maramire@usp.br

Wesley Beccaro - USP - wesleybeccaro@usp.br
