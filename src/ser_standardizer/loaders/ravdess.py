import os
import pandas as pd

# Formato dos arquivos: Modality-VocalChannel-Emotion-Intensity-Statement-Repetition-Actor.wav
EMOTION_MAP = {
    '01': 'Neutral',
    '02': 'Calm',      # juntar com 01
    '03': 'Happy',
    '04': 'Sad',
    '05': 'Anger',
    '06': 'Fear',
    '07': 'Disgust',
    '08': 'Surprise'
}

# Sao apenas duas mesmo
SENTENCE_MAP = {
    '01': "Kids are talking by the door",
    '02': "Dogs are sitting by the door"
}

def process(base_dir):
    """
    Processa o dataset RAVDESS (Arquivos de áudio Speech).
    
    A estrutura padrão do RAVDESS extraído costuma ser:
    base_dir/
        Actor_01/
            03-01-01-01-01-01-01.wav
        Actor_02/
            ...
            
    Args:
        base_dir (str): Caminho raiz para o dataset RAVDESS.

    Returns:
        pandas.DataFrame: DataFrame padronizado.
    """
    print("Iniciando processamento do RAVDESS...")

    all_file_data = []

    # Caminha por todas as subpastas (Actor_01, Actor_02, etc.)
    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            if filename.endswith('.wav'):
                # Exemplo de nome: 03-01-06-01-02-01-12.wav
                file_key = os.path.splitext(filename)[0]
                parts = file_key.split('-')

                # Verifica se o nome do arquivo segue o padrão de 7 partes do RAVDESS
                if len(parts) != 7:
                    continue

                # --- Extração dos Códigos ---
                modality = parts[0]      # 01=Video-only, 02=Video+Audio, 03=Audio-only
                vocal_channel = parts[1] # 01=Speech, 02=Song
                emotion_code = parts[2]
                intensity = parts[3]     # 01=Normal, 02=Strong
                statement_code = parts[4]
                repetition = parts[5]
                actor_id = parts[6]

                if vocal_channel != '01': # Apenas speech (tira song)
                    continue

                try:
                    full_file_path = os.path.join(root, filename)

                    # --- Gênero ---
                    # Ímpar = Masculino, Par = Feminino
                    actor_num = int(actor_id)
                    gender = 'Female' if actor_num % 2 == 0 else 'Male'

                    # --- Montagem dos Dados ---
                    file_info = {
                        'dataset': 'RAVDESS',
                        'file_path': full_file_path,
                        # 'filename': filename,
                        'speaker_id': f"ravdess_{actor_id}",
                        'gender': gender,
                        'language': 'en',
                        'sentence_text': SENTENCE_MAP.get(statement_code, "Unknown"),
                        'emotion': EMOTION_MAP.get(emotion_code, 'Unknown'),
                        # 'intensity': 'Normal' if intensity == '01' else 'Strong'
                    }

                    all_file_data.append(file_info)

                except Exception as e:
                    print(f"Erro ao processar arquivo {filename}: {e}")

    print(f"Processamento do RAVDESS concluído. {len(all_file_data)} arquivos processados.")

    if not all_file_data:
        return None

    # --- Criar e Retornar o DataFrame ---
    final_df = pd.DataFrame(all_file_data)

    standard_columns = [
        'dataset', 'file_path', 'speaker_id', 'gender',
        'emotion', 'sentence_text', 'language'
    ]

    # Garante que todas as colunas existam (segurança)
    for col in standard_columns:
        if col not in final_df:
            final_df[col] = pd.NA

    return final_df[standard_columns]