# SER-Standardizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

**Uma infraestrutura modular para padronização de datasets e extração de características em Reconhecimento de Emoção na Fala (SER).**

O **SER-Standardizer** é um pacote Python desenvolvido para unificar a formatação de múltiplos bancos de dados de voz, mitigando a heterogeneidade de metadados. O objetivo principal é facilitar o treinamento cruzado (*cross-corpus training*) e testes de generalização de modelos de aprendizado de máquina.

Além do pipeline de padronização, a ferramenta conta com um módulo de extensão para extração de características acústicas (espectrais e prosódicas) integrando o framework **openSMILE**.

## 📋 Datasets Suportados Atualmente

A ferramenta atualmente suporta o carregamento e padronização dos seguintes bancos de dados:

* **CREMA-D** | **IEMOCAP** | **SAVEE** | **EmoUERJ** (PT-BR) | **MSP-IMPROV** | **RAVDESS**

## 🚀 Instalação

### Pré-requisitos
* Python 3.8 ou superior
* Bibliotecas listadas no `pyproject.toml` (instaladas automaticamente).

### Instalação via código fonte
Clone este repositório para instalar utilizando o `pip` (leia mais abaixo sobre isso):
```
git clone https://github.com/ViniciusSuaiden/ser-standardizer.git
cd ser-standardizer
```

A biblioteca foi projetada com flexibilidade em mente, oferecendo duas modalidades de instalação para otimizar o uso de recursos computacionais:

#### 1. Instalação Base (Metadados Leve) 
Instala apenas os pacotes essenciais (`pandas`, `audb`) para a padronização e filtragem tabular.
```bash
pip install .
```
#### 2. Instalação Completa (Com Processamento de Sinais)
Instala as dependências pesadas necessárias para o módulo de extração de características e manipulação de áudio (opensmile, noisereduce).
```bash
pip install '.[features]'
```
### 💻 Como Usar
O fluxo de trabalho é dividido em três etapas lógicas:

**1. Pré-processamento (CLI)**

Após a instalação, o comando ser-std estará disponível no seu terminal.
Para padronizar um dataset específico:
```bash
# Exemplo: crema_d
ser-std --dataset crema_d --input_dir /caminho/para/crema
```
O arquivo `.csv` padronizado é inserido na pasta base do usuário, com nomes específicos para cada banco de dados.

**2. Manipulação e Filtragem de Dados (Python)**

Após o pré-processamento, utilize a biblioteca para carregar, filtrar e manipular os áudios diretamente em seu código ou Jupyter Notebook.
```python
import ser_standardizer as ser

# Carrega múltiplos datasets padronizados em um único DataFrame
df = ser.load_datasets(["crema_d", "ravdess", "iemocap"])

# Filtra por dataset, emoção e gênero
df_target = ser.filters(
    df,
    datasets=['ravdess', 'iemocap'],
    emotions=['anger', 'sad'], 
    genders=['female']
)
```
**3. Extração de Características Acústicas (Requer [features])**

O módulo de extração automatiza o processamento digital de sinais. Ele inclui a opção de aplicar uma máscara de Detecção de Atividade de Voz (VAD) baseada na energia RMS para extrair características estritamente dos trechos de fonação efetiva.
```python
# Extração massiva via openSMILE
# 'feature_set' suportados: 'eGeMAPS' ou 'ComParE'
features_df = ser.extract_features(
    df_target, 
    feature_set='eGeMAPS',
    use_vad=True, # Remove silêncio antes da extração
    sr=16000      # Taxa de amostragem
)

# O resultado preserva os índices originais, facilitando a concatenação
import pandas as pd
dataset_final = pd.concat([df_target, features_df], axis=1)

# --- Utilitários Extras ---
# Escutar o áudio no Jupyter Notebook
ser.listen(df_target, index=42)

# Carregar o áudio puro em NumPy Array (ex: para alimentar Redes Neurais)
audio_array = ser.load_audio(df_target, index=42)

# Carregar um lote de áudios com Zero-Padding
batch = ser.load_batch(df_target, begin=0, end=32)
```

### ✍️ Autores
Vinicius Suaiden - USP - vinicius.suaiden@usp.br

Miguel Arjona Ramirez - USP - maramire@usp.br

Wesley Beccaro - USP - wesleybeccaro@usp.br
