import pandas as pd
import audb
import os

EMOTION_MAP = {
    'anger': 'Anger',
    'happiness': 'Happy',
    'sadness': 'Sad',
    'neutral': 'Neutral'
}

def process(base_dir=None):
    """
    Carrega o dataset EmoUERJ via audb e padroniza para o formato do projeto.
    
    Args:
        base_dir (str): Opcional neste caso, pois o audb gerencia o cache.
                        Pode ser usado para definir onde o audb salva os arquivos
                        se você configurar o cache localmente.

    Returns:
        pandas.DataFrame: DataFrame padronizado.
    """
    print("Iniciando processamento do EmoUERJ via audb...")

    try:
        db = audb.load("emouerj", version="1.0.0", verbose=False)

        original_df = db.get("emotion", ["gender", "speaker", "take"])
        
        original_df['file_path'] = original_df.index
        original_df = original_df.reset_index(drop=True)

        print(f"EmoUERJ carregado. Processando {len(original_df)} arquivos...")

        all_file_data = []

        for row in original_df.itertuples():
            try:
                original_emotion = row.emotion
                speaker = row.get('speaker')
                gender = row.get('gender').capitalize()
                full_path = row.get('file_path')
                filename = os.path.basename(full_path)
                sentence_text = "Conteúdo em Português" 

                file_info = {
                    'dataset': 'EmoUERJ',
                    'file_path': full_path,
                    # 'filename': filename,
                    'speaker_id': f"emouerj_{speaker}",
                    'gender': gender,
                    'language': 'pt-br',
                    'sentence_text': sentence_text,
                    'emotion': EMOTION_MAP.get(original_emotion, original_emotion),
                }

                all_file_data.append(file_info)

            except Exception as e:
                print(f"Erro ao processar linha do EmoUERJ: {e}")

        final_df = pd.DataFrame(all_file_data)
        
        standard_columns = [
            'dataset', 'file_path', 'speaker_id', 'gender',
            'emotion', 'sentence_text', 'language'
        ]

        for col in standard_columns:
            if col not in final_df:
                final_df[col] = pd.NA

        print(f"Processamento do EmoUERJ concluído. {len(final_df)} arquivos.")
        return final_df[standard_columns]

    except Exception as e:
        print(f"Falha crítica ao carregar EmoUERJ via audb: {e}")
        return None