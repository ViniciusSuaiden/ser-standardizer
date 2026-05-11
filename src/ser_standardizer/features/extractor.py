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
        feature_level: 'functionals' (estatísticas globais por arquivo) ou 'llds' (nível de frame).
        use_vad: Se True, remove silêncios baseados na energia RMS. 
                 ATENÇÃO: Permitido apenas quando feature_level='llds'.
        sr: Taxa de amostragem esperada.
        
    Returns:
        Um novo pd.DataFrame contendo as features. 
        Para 'functionals', mantém o índice original.
        Para 'llds', adiciona o índice original ('file_idx') para cruzamento de metadados.
    """

    if use_vad and feature_level.lower() == 'functionals':
        raise ValueError(
            "Erro de Metodologia: A aplicação de VAD no áudio bruto antes da extração "
            "de funcionais corrompe as métricas temporais padronizadas do openSMILE "
            "(como taxa de fala e proporção de pausas) e introduz artefatos no espectro. \n"
            "-> Para extrair 'functionals' padronizados, defina use_vad=False. \n"
            "-> O uso de use_vad=True é permitido apenas para extração no nível de frame ('llds')."
        )

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
            
            if flevel == opensmile.FeatureLevel.Functionals:
                feat_series = feat_df.iloc[0].rename(idx)
                features_list.append(feat_series)
            else:
                feat_df['file_idx'] = idx 
                features_list.append(feat_df)
                
        except Exception as e:
            print(f"Erro na extração do índice {idx}: {e}")
            if flevel == opensmile.FeatureLevel.Functionals:
                features_list.append(pd.Series(dtype=float, name=idx))
            else:
                features_list.append(pd.DataFrame({'file_idx': [idx]}))

    print("Consolidando matriz de features...")
    
    if flevel == opensmile.FeatureLevel.Functionals:
        result_df = pd.DataFrame(features_list)
    else:
        result_df = pd.concat(features_list)
        if 'file_idx' in result_df.columns:
            result_df = result_df.set_index('file_idx', append=True)
            
    return result_df