import pandas as pd
import os
from pathlib import Path

def load(datasets):
    """
    Carrega um ou múltiplos datasets padronizados em um único DataFrame.
    Pode passar o nome como string ('crema_d') ou lista (['crema_d', 'iemocap']).
    """
    
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