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
**Uso via Linha de Comando (CLI)**

Após a instalação, o comando ser-std estará disponível no seu terminal.
Para padronizar um dataset específico:
```bash
# Exemplo: crema_d
ser-std --dataset crema_d --input_dir /caminho/para/crema --output_csv /caminho/para/saida
```

### ✍️ Autores
Vinicius Suaiden - USP - vinicius.suaiden@usp.br

Miguel Arjona Ramirez - USP - maramire@usp.br

Wesley Beccaro - USP - wesleybeccaro@usp.br
