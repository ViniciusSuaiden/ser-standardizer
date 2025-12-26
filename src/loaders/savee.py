import os
import pandas as pd

def process(base_dir):
    """
    Processa o arquivo PARQUET do SAVEE (baixado localmente),
    consolida os metadados e retorna um DataFrame padronizado.
    
    Args:
        base_dir (str): O caminho para a pasta que CONTÉM
                        o arquivo .parquet do SAVEE.
                        (ex: ".../Datasets/SAVEE")

    Returns:
        pandas.DataFrame: Um DataFrame com metadados padronizados
                          ou None se o processamento falhar.
    """
    print("Iniciando processamento do SAVEE (Parquet Local)...")

    try:
        parquet_path = os.path.join(base_dir, "savee_hf_data.parquet")
        print(f"Carregando arquivo: {parquet_path}")
        df = pd.read_parquet(parquet_path)

    except Exception as e:
        print(f"Erro ao ler o arquivo Parquet do SAVEE: {e}")
        return None

    print("Arquivo Parquet carregado. Iniciando mapeamento para o formato padrão...")

    try:
        final_df = pd.DataFrame()
        # final_df['filename'] = df['file'] 
        final_df['dataset'] = 'SAVEE'
        final_df['file_path'] = pd.NA # POR ENQUANTO
        final_df['speaker_id'] = 'savee_' + df['file'].str.split('_').str[0]
        final_df['gender'] = df['gender'].str.capitalize() 
        final_df['emotion'] = df['emotion'].str.capitalize() 
        final_df['sentence_text'] = df['transcription']
        final_df['language'] = 'en'

        standard_columns_to_add = [
            'intensity', 'race', 'ethnicity', 
            'perceived_emotion', 'perceived_emotion_agreement'
        ]
        for col in standard_columns_to_add:
            final_df[col] = pd.NA

        standard_columns = [
            'dataset', 'file_path', 'speaker_id', 'gender',
            'emotion', 'sentence_text', 'language'
        ]
        
        final_df = final_df[standard_columns]
        
        print(f"Processamento do SAVEE concluído. {len(final_df)} arquivos processados.")
        
        return final_df

    except KeyError as e:
        print(f"Erro: O arquivo Parquet não contém a coluna esperada: {e}.")
        return None
    except Exception as e:
        print(f"Erro inesperado ao transformar o DataFrame do SAVEE: {e}")
        return None