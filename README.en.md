# SER-Standardizer

[🇧🇷 Português](README.md) | 🇺🇸 English

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

**A modular infrastructure for dataset standardization and feature extraction in Speech Emotion Recognition (SER).**

**SER-Standardizer** is a Python package built to unify the formatting of multiple speech databases, mitigating metadata heterogeneity. Its main goal is to facilitate *cross-corpus training* and generalization testing of machine learning models.

Beyond the standardization pipeline, the tool provides an extension module for acoustic feature extraction (spectral and prosodic) by integrating the **openSMILE** framework.

## 📋 Currently Supported Datasets

The tool currently supports loading and standardizing the following databases:

* **CREMA-D** | **IEMOCAP** | **EmoUERJ** (PT-BR) | **MSP-IMPROV** | **MSP-PODCAST** | **RAVDESS** | **EmoDB** (DE)

Per-dataset download and directory-layout guides are available under [`docs/en/datasets/`](docs/en/datasets/).

## 🚀 Installation

### Prerequisites
* Python 3.8 or higher
* Libraries listed in `pyproject.toml` (installed automatically).

### Installation from source
Clone this repository to install it with `pip` (read more about it below):
```
git clone https://github.com/ViniciusSuaiden/ser-standardizer.git
cd ser-standardizer
```

The library was designed with flexibility in mind, offering two installation modes to optimize the use of computational resources:

#### 1. Base Installation (Lightweight Metadata)
Installs only the essential packages (`pandas`, `audb`) for tabular standardization and filtering.
```bash
pip install .
```
#### 2. Full Installation (With Signal Processing)
Installs the heavy dependencies required for the feature extraction and audio manipulation module (opensmile, noisereduce).
```bash
pip install '.[features]'
```
### 💻 How to Use
The workflow is split into three logical steps:

**1. Preprocessing (CLI)**

After installation, the `ser-std` command becomes available in your terminal.
To standardize a specific dataset:
```bash
# Example: crema_d
ser-std --dataset crema_d --input_dir /path/to/crema
```
The standardized `.csv` file is written to the user's home folder, with a specific name for each database.

**2. Data Handling and Filtering (Python)**

After preprocessing, use the library to load, filter and manipulate the audio directly in your code or Jupyter Notebook.
```python
import ser_standardizer as ser

# Loads multiple standardized datasets into a single DataFrame
df = ser.load_datasets(["crema_d", "ravdess", "iemocap"])

# Filters by dataset, emotion and gender
df_target = ser.filters(
    df,
    datasets=['ravdess', 'iemocap'],
    emotions=['anger', 'sad'],
    genders=['female']
)
```
**3. Acoustic Feature Extraction (Requires [features])**

The extraction module automates digital signal processing. It includes the option to apply a Voice Activity Detection (VAD) mask based on RMS energy to extract features strictly from the effective phonation segments.
```python
# Batch extraction via openSMILE
# Supported 'feature_set' values: 'eGeMAPS' or 'ComParE'
features_df = ser.extract_features(
    df_target,
    feature_set='eGeMAPS',
    feature_level='functionals', # 'functionals' (1 vector per utterance) or 'llds' (per frame)
    use_vad=False, # VAD (silence removal) is only allowed with feature_level='llds'
    sr=16000       # Sampling rate
)

# The result preserves the original indices, making concatenation easy
import pandas as pd
final_dataset = pd.concat([df_target, features_df], axis=1)

# --- Extra Utilities ---
# Listen to the audio in a Jupyter Notebook
ser.listen(df_target, index=42)

# Load the raw audio as a NumPy array (e.g., to feed neural networks)
audio_array = ser.load_audio(df_target, index=42)

# Load a batch of audio with zero-padding
batch = ser.load_batch(df_target, begin=0, end=32)
```

### ✍️ Authors
Vinicius Suaiden - USP - vinicius.suaiden@usp.br

Miguel Arjona Ramirez - USP - maramire@usp.br

Wesley Beccaro - USP - wesleybeccaro@usp.br
