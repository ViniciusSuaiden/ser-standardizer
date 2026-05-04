import pandas as pd
import os
from pathlib import Path

def load_datasets(datasets):
    if isinstance(datasets, str):
        target_datasets = [datasets]
    else:
        target_datasets = datasets

    dataframes = []
    DATA_DIR = os.path.join(Path.home(), ".ser_standardizer_data")
    
    for name in target_datasets:
        file_path = os.path.join(DATA_DIR, f"process_{name}.csv")
        if not file_path or not os.path.exists(file_path):
            raise FileNotFoundError(
                f"O dataset '{name}' não foi encontrado. "
                f"Certifique-se de ter rodado: ser-std --dataset {name} ..."
            )
        df = pd.read_csv(file_path)
        dataframes.append(df)

    if not dataframes:
        raise ValueError("Nenhum dataset válido foi fornecido.")
        
    return pd.concat(dataframes, ignore_index=True)

def filters(df, datasets=None, emotions=None, genders=None, languages=None):
    mask = pd.Series([True] * len(df), index=df.index)

    def to_list(val):
        if isinstance(val, str):
            return [val]
        return val
    
    if datasets:
        target = [x.lower() for x in to_list(datasets)]
        mask = mask & df['dataset'].str.lower().isin(target)

    if emotions:
        target = [x.lower() for x in to_list(emotions)]
        mask = mask & df['emotion'].str.lower().isin(target)

    if genders:
        target = [x.lower() for x in to_list(genders)]
        mask = mask & df['gender'].str.lower().isin(target)
        
    if languages:
        target = [x.lower() for x in to_list(languages)]
        mask = mask & df['language'].str.lower().isin(target)
    
    print(f"Filtro aplicado. Restaram {len(df[mask])} amostras.")
    return df[mask].copy()

try:
    from .features.preprocessing import listen, load_audio, load_batch, mean_energy
    from .features.extractor import extract_features
    FEATURES_AVAILABLE = True

except ImportError:
    FEATURES_AVAILABLE = False
    
    def _missing_deps_error(*args, **kwargs):
        raise ImportError(
            "Esta função requer o submódulo de extração acústica.\n"
            "Para utilizá-la, reinstale o pacote com as dependências completas:\n\n"
            "    pip install '.[features]'"
        )
        
    listen = load_audio = load_batch = mean_energy = extract_features = _missing_deps_error