import pandas as pd
import numpy as np
from tqdm.auto import tqdm
import opensmile
from .preprocessing import load_audio, remove_silence

def extract_features(df, feature_set='eGeMAPS', feature_level='functionals', use_vad=False, sr=16000):
    """
    Extrai características acústicas utilizando o openSMILE.
    
    Args:
        df: DataFrame contendo a coluna 'file_path'.
        feature_set: 'eGeMAPS' ou 'ComParE' (padrões validados na literatura).
        feature_level: 'functionals' (estatísticas por arquivo) ou 'llds' (nível de frame).
        use_vad: Se True, aplica a máscara de silêncio antes da extração.
        sr: Taxa de amostragem esperada.
        
    Returns:
        Um novo pd.DataFrame contendo as features. 
        Para 'functionals', mantém o índice original.
        Para 'llds', adiciona o índice original ('file_idx') para cruzamento de metadados.
    """

    # 1. Definir o Conjunto de Features
    if feature_set.lower() == 'egemaps':
        fset = opensmile.FeatureSet.eGeMAPSv02
    elif feature_set.lower() == 'compare':
        fset = opensmile.FeatureSet.ComParE_2016
    else:
        raise ValueError("Conjunto não suportado. Escolha 'eGeMAPS' ou 'ComParE'.")

    # 2. Definir o Nível da Extração
    if feature_level.lower() == 'functionals':
        flevel = opensmile.FeatureLevel.Functionals
        level_name = "Functionals"
    elif feature_level.lower() in ['lld', 'llds']:
        flevel = opensmile.FeatureLevel.LowLevelDescriptors
        level_name = "LowLevelDescriptors"
    else:
        raise ValueError("Nível não suportado. Escolha 'functionals' ou 'llds'.")

    print(f"Inicializando openSMILE ({feature_set} - {level_name})...")
    smile = opensmile.Smile(
        feature_set=fset,
        feature_level=flevel,
    )
    
    features_list = []
    
    # 3. Processamento
    for idx in tqdm(df.index, desc=f"Extraindo características ({level_name})"):
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
            
            # Tratamento diferente com base no nível escolhido
            if flevel == opensmile.FeatureLevel.Functionals:
                feat_series = feat_df.iloc[0].rename(idx)
                features_list.append(feat_series)
            else:
                feat_df['file_idx'] = idx 
                features_list.append(feat_df)
                
        except Exception as e:
            print(f"Erro na extração do índice {idx}: {e}")
            # Tratamento de erro compatível com o nível
            if flevel == opensmile.FeatureLevel.Functionals:
                features_list.append(pd.Series(dtype=float, name=idx))
            else:
                features_list.append(pd.DataFrame({'file_idx': [idx]}))

    print("Consolidando matriz de features...")
    
    # 4. Consolidação
    if flevel == opensmile.FeatureLevel.Functionals:
        result_df = pd.DataFrame(features_list)
    else:
        result_df = pd.concat(features_list)
        if 'file_idx' in result_df.columns:
            result_df = result_df.set_index('file_idx', append=True)
            
    return result_df