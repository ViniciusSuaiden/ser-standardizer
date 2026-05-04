import pandas as pd
import numpy as np
from tqdm.auto import tqdm
import opensmile
from .preprocessing import load_audio, remove_silence

def extract_features(df, feature_set='eGeMAPS', use_vad=False, sr=16000):
    """
    Extrai características acústicas utilizando o openSMILE.
    
    Args:
        df: DataFrame contendo a coluna 'file_path'.
        feature_set: 'eGeMAPS' ou 'ComParE' (padrões validados na literatura).
        use_vad: Se True, aplica a máscara de silêncio antes da extração.
        sr: Taxa de amostragem esperada.
        
    Returns:
        Um novo pd.DataFrame contendo as features, com os mesmos índices do df original.
    """

    if feature_set.lower() == 'egemaps':
        fset = opensmile.FeatureSet.eGeMAPSv02
    elif feature_set.lower() == 'compare':
        fset = opensmile.FeatureSet.ComParE_2016
    else:
        raise ValueError("Conjunto não suportado. Escolha 'eGeMAPS' ou 'ComParE'.")

    print(f"Inicializando openSMILE ({feature_set})...")
    smile = opensmile.Smile(
        feature_set=fset,
        feature_level=opensmile.FeatureLevel.Functionals,
    )
    
    features_list = []
    

    for idx in tqdm(df.index, desc="Extraindo características"):
        file_path = df.loc[idx, 'file_path']
        
        try:
            if use_vad:
                audio = load_audio(df, idx, sr=sr)
                audio_clean = remove_silence(audio, sr=sr)
                
                if len(audio_clean) == 0:
                    audio_clean = np.zeros(sr)
                    
                feat_df = smile.process_signal(audio_clean, sr)
            else:
                feat_df = smile.process_file(file_path)
                
            feat_series = feat_df.iloc[0].rename(idx)
            features_list.append(feat_series)
            
        except Exception as e:
            print(f"Erro na extração do índice {idx}: {e}")
            features_list.append(pd.Series(dtype=float, name=idx))

    print("Consolidando matriz de features...")
    result_df = pd.DataFrame(features_list)
    
    return result_df