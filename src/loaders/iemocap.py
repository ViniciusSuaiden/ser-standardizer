import os
import re
import pandas as pd

EMOTION_MAP = {
    'ang': 'Anger',
    'hap': 'Happy', 
    'exc': 'Excited', # juntar com hap
    'sad': 'Sad',
    'neu': 'Neutral',
    'fru': 'Frustration',
    'fea': 'Fear',
    'sur': 'Surprise',
    'dis': 'Disgust',
    'oth': 'Other',
    'xxx': 'Unknown'
}

def parse_transcriptions(transcription_path):
    """
    Lê o arquivo de transcrição e retorna um dicionário {utterance_id: text}.
    """
    transcriptions = {}
    if not os.path.exists(transcription_path):
        return transcriptions

    with open(transcription_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Formato típico: "Ses01F_impro01_F000 [time]: Texto falado"
            parts = line.strip().split(']: ')
            if len(parts) >= 2:
                header = parts[0].split(' [')[0] 
                text = parts[1]
                transcriptions[header] = text
    return transcriptions

def process(base_dir):
    """
    Processa o dataset IEMOCAP (estrutura de Sessões 1 a 5).
    
    Args:
        base_dir (str): Caminho raiz onde estão as pastas Session1, Session2, etc.
        
    Returns:
        pandas.DataFrame: DataFrame padronizado.
    """
    print("Iniciando processamento do IEMOCAP...")
    
    all_file_data = []
    
    # O IEMOCAP é dividido em 5 sessões
    sessions = ['Session1', 'Session2', 'Session3', 'Session4', 'Session5']
    
    for session in sessions:
        session_dir = os.path.join(base_dir, session)
        if not os.path.isdir(session_dir):
            print(f"Aviso: {session} não encontrada em {base_dir}. Pulando...")
            continue
            
        print(f"Processando {session}...")
        
        # Caminhos cruciais dentro da sessão
        wav_root = os.path.join(session_dir, 'dialog', 'wav')
        label_root = os.path.join(session_dir, 'dialog', 'EmoEvaluation')
        trans_root = os.path.join(session_dir, 'dialog', 'transcriptions')
        
        # Iterar sobre os arquivos de rótulos (cada arquivo corresponde a uma conversa/cena)
        if not os.path.exists(label_root):
            print(f"Pasta de rótulos não encontrada para {session}. Pulando.")
            continue

        for label_file in os.listdir(label_root):
            if not label_file.endswith('.txt') or label_file.startswith('.'):
                continue
                
            label_path = os.path.join(label_root, label_file)
            
            # Nome da cena (ex: Ses01F_impro01)
            scene_name = os.path.splitext(label_file)[0]
            
            # Carregar transcrições correspondentes a esta cena para memória
            transcription_file = os.path.join(trans_root, scene_name + '.txt')
            scene_transcriptions = parse_transcriptions(transcription_file)
            
            with open(label_path, 'r') as f:
                lines = f.readlines()
                
            for line in lines:
                # Exemplo: [6.2901 - 8.2357]	Ses01F_impro01_F000	neu	[2.0000, 2.5000, 2.5000]
                match = re.search(r"\[(\d+\.\d+) - (\d+\.\d+)\]\t(\w+)\t(\w+)\t", line)
                
                if match:
                    utterance_id = match.group(3)
                    raw_emotion = match.group(4)
                    
                    # Verificar caminho do áudio
                    wav_filename = f"{utterance_id}.wav"
                    full_wav_path = os.path.join(wav_root, scene_name, wav_filename)
                    
                    # Extração de metadados pelo ID (Ex: Ses01F_impro01_F000)
                    parts = utterance_id.split('_')
                    last_part = parts[-1] # F000 ou M001
                    speaker_code = last_part[0]
                    
                    # Ses01 tem M01 e F01. 
                    session_num = session[-1] # '1'
                    speaker_id = f"iemocap_Ses{session_num}_{speaker_code}"
                    
                    gender_map = {'F': 'Female', 'M': 'Male'}
                    gender = gender_map.get(speaker_code, 'Unknown')
                    
                    # Buscar texto
                    text = scene_transcriptions.get(utterance_id, "Transcr. não encontrada")
                    
                    file_info = {
                        'dataset': 'IEMOCAP',
                        'file_path': full_wav_path,
                        # 'filename': wav_filename,
                        'speaker_id': speaker_id,
                        'gender': gender,
                        'language': 'en',
                        'sentence_text': text,
                        'emotion': EMOTION_MAP.get(raw_emotion, raw_emotion),
                    }
                    
                    all_file_data.append(file_info)

    print(f"Processamento do IEMOCAP concluído. {len(all_file_data)} arquivos mapeados.")
    
    if not all_file_data:
        return None

    final_df = pd.DataFrame(all_file_data)
    
    standard_columns = [
        'dataset', 'file_path', 'speaker_id', 'gender',
        'emotion', 'sentence_text', 'language'
    ]
    
    return final_df[standard_columns]