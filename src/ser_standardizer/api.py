import pandas as pd
import os
from pathlib import Path
import librosa
import numpy as np
from IPython.display import Audio, display

def load_datasets(datasets):
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

def listen(df, index):
    """
    Reproduz o áudio diretamente no Jupyter Notebook.
    """
    path = df.loc[index, 'file_path']
    emotion = df.loc[index, 'emotion']
    print(f"Tocando áudio {index} | Emoção: {emotion}")
    
    display(Audio(filename=path))

def load_audio(df, index, sr=16000):
    """
    Retorna o array numpy de UM áudio específico.
    """
    if index not in df.index:
        raise IndexError("Índice não encontrado no Dataset.")
        
    path = df.loc[index, 'file_path']

    audio, _ = librosa.load(path, sr=sr) 
    return audio

def load_batch(df, begin, end, sr=16000, max_1000=True):
    """
    Carrega um intervalo de áudios baseado na posição (iloc).
    """
    qtd = end - begin
    
    if qtd > 1000 and max_1000:
        raise ValueError(f"Você tentou carregar {qtd} áudios. O limite é 1000. Defina max_1000=False se tiver certeza.")

    batch = []
    
    subset_indices = df.index[begin:end]

    for idx in subset_indices:
        try:
            audio = load_audio(df, idx, sr)
            batch.append(audio)
        except Exception as e:
            print(f"Erro ao carregar índice {idx}: {e}")
            batch.append(None)

    max_len = max(len(x) for x in batch)

    padded_batch = np.zeros((len(batch), max_len), dtype=np.float32)

    for i, audio in enumerate(batch):
        padded_batch[i, :audio.shape[0]] = audio
            
    return padded_batch

def filters(df, datasets=None, emotions=None, genders=None, languages=None):
    """
    Filtra o dataset com base em critérios múltiplos.
    
    Args:
        datasets: Nome(s) do dataset (ex: 'crema_d' ou ['crema_d', 'ravdess'])
        emotions: Emoção(ões) (ex: 'anger' ou ['anger', 'happy'])
        genders: Gênero (ex: 'female')
        languages: Idioma(s) (ex: 'en')
        
    Returns:
        Uma NOVA instância da classe contendo apenas os dados filtrados.
    """

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
    
    print(f"Filtro aplicado. Restaram {len(df[mask])} áudios.")
    return df[mask].copy()