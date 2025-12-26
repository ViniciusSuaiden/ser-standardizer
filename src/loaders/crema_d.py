import os
import pandas as pd

SENTENCE_MAP = {
    "IEO": "It's eleven o'clock.",
    "TIE": "That is exactly what happened.",
    "IOM": "I'm on my way to the meeting.",
    "IWW": "I wonder what this is about.",
    "TAI": "The airplane is almost full.",
    "MTI": "Maybe tomorrow it will be cold.",
    "IWL": "I would like a new alarm clock.",
    "ITH": "I think I have a cold.",
    "DFA": "Don't forget a jacket.",
    "ITS": "I think I'll wear my new suit.",
    "TSI": "The surface is slick.",
    "WSI": "We'll stop in a couple of minutes."
}

EMOTION_MAP = {
    'A': 'Anger',
    'D': 'Disgust',
    'F': 'Fear',
    'H': 'Happy',
    'S': 'Sad',
    'N': 'Neutral',
}

def process(base_dir=None):
    """
    Processa todos os arquivos de áudio do dataset CREMA-D,
    consolida os metadados e retorna um DataFrame padronizado.
    
    Args:
        base_dir (str): O caminho raiz para o dataset CREMA-D 
                        (ex: ".../data/CREMA-D")

    Returns:
        pandas.DataFrame: Um DataFrame com metadados padronizados
                          ou None se o processamento falhar.
    """
    print("Iniciando processamento do CREMA-D...")

    # --- Definir Caminhos ---
    if base_dir is None:
        base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "CREMA-D")
    else:
        base_dir = os.path.abspath(base_dir)
    AUDIO_DIR = os.path.join(base_dir, "AudioWAV")
    DEMOGRAPHICS_FILE = os.path.join(base_dir, "VideoDemographics.csv")
    RESPONSES_FILE = os.path.join(base_dir, "finishedResponses.csv")

    # --- Carregar Metadados ---
    print("Carregando arquivos de metadados do CREMA-D...")
    try:
        demographics_df = pd.read_csv(DEMOGRAPHICS_FILE).set_index('ActorID')
        
        raw_responses_df = pd.read_csv(RESPONSES_FILE, usecols=['queryType', 'clipName', 'respEmo'])
        voice_responses_df = raw_responses_df[raw_responses_df['queryType'] == 1].copy()

        votes_df = pd.crosstab(voice_responses_df['clipName'], voice_responses_df['respEmo'])
        emotion_columns = ['A', 'D', 'F', 'H', 'S', 'N']
                
        votes_df['perceived_emotion_label'] = votes_df[emotion_columns].idxmax(axis=1)
        print("Arquivos de metadados do CREMA-D carregados com sucesso.")

    except Exception as e:
        print(f"Erro ao carregar os arquivos CSV do CREMA-D: {e}")
        return None

    # --- Iterar sobre os arquivos de áudio ---
    print(f"Iniciando processamento dos arquivos em: {AUDIO_DIR}")
    all_file_data = []

    for filename in os.listdir(AUDIO_DIR):
        if filename.endswith('.wav'):
            full_file_path = os.path.join(AUDIO_DIR, filename)
            file_key = os.path.splitext(filename)[0]
            
            try:
                # --- A. Extrair dados do NOME DO ARQUIVO ---
                parts = file_key.split('_')
                actor_id = int(parts[0])
                sentence_id = parts[1]
                intended_emotion_code = parts[2]
                
                # --- B. Buscar dados dos CSVs carregados ---
                speaker_gender = demographics_df.loc[actor_id]['Sex']
                sentence_text = SENTENCE_MAP.get(sentence_id, "Desconhecido")
                perceived_emotion_code = votes_df.loc[file_key]['perceived_emotion_label']
                
                # --- C. Padronizar e Consolidar ---
                file_info = {
                    'dataset': 'CREMA-D',
                    'file_path': full_file_path,
                    # 'filename': filename,
                    'speaker_id': f"crema_{actor_id}", 
                    'gender': speaker_gender,
                    'language': 'en',
                    'sentence_text': sentence_text,
                    'emotion': EMOTION_MAP.get(perceived_emotion_code, perceived_emotion_code),
                }
                
                all_file_data.append(file_info)

            except KeyError as e:
                print(f"Aviso: Não foi possível encontrar metadados para {filename}. Chave não encontrada: {e}. Pulando...")
            except Exception as e:
                print(f"Erro ao processar o arquivo {filename}: {e}. Pulando...")

    print(f"Processamento do CREMA-D concluído. {len(all_file_data)} arquivos processados.")

    if not all_file_data:
        return None

    # --- 4. Criar e Retornar o DataFrame ---
    final_df = pd.DataFrame(all_file_data)
    
    # Reordenar colunas para um layout padrão
    standard_columns = [
        'dataset', 'file_path', 'speaker_id', 'gender',
        'emotion', 'sentence_text', 'language'
    ]
    
    # Adiciona colunas que podem não existir no DF final (caso dê erro em todas)
    for col in standard_columns:
        if col not in final_df:
            final_df[col] = pd.NA
            
    return final_df[standard_columns]