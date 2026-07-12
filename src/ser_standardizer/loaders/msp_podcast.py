import os
import pandas as pd

# --- MAPS ---
# Emoção primária de consenso (coluna EmoClass em labels_consensus.csv)
EMOTION_MAP = {
    'A': 'Anger', 'S': 'Sad', 'H': 'Happy', 'U': 'Surprise',
    'F': 'Fear', 'D': 'Disgust', 'C': 'Contempt', 'N': 'Neutral',
    'O': 'Other', 'X': 'Unknown'  # X = "No agreement" (sem vencedor por pluralidade)
}

# --- HELPERS ---

def load_transcriptions(base_dir):
    """
    Carrega as transcrições da pasta 'Transcripts' (arquivos .txt), caso ela exista.
    Retorna { 'MSP-PODCAST_XXXX_YYYY': 'texto' }.
    """
    trans_map = {}
    trans_dir = os.path.join(base_dir, "Transcripts")

    if os.path.exists(trans_dir) and os.path.isdir(trans_dir):
        print(f"Loading transcriptions from {trans_dir}...")
        for root, _, files in os.walk(trans_dir):
            for file in files:
                if file.endswith(".txt"):
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                            text = f.read().strip()
                            key = os.path.splitext(file)[0]
                            trans_map[key] = text
                    except:
                        pass
    return trans_map

# --- MAIN PROCESS ---

def process(base_dir):
    """
    Processa o dataset MSP-PODCAST a partir do arquivo de consenso 'labels_consensus.csv'.

    Este arquivo já traz, por turno de fala, a emoção primária de consenso, o gênero,
    o identificador do falante e a partição sugerida (Train/Development/Test1/Test2).
    A partição Test3 não é distribuída com labels e, portanto, não aparece aqui.

    Os áudios ('Audios/') não precisam estar presentes: o caminho esperado do .wav é
    montado a partir do nome do arquivo, permitindo padronizar os metadados mesmo sem
    o áudio em disco.

    Estrutura esperada em base_dir:
        base_dir/
            Labels/
                labels_consensus.csv
            Audios/          <-- opcional (.wav, nomes achatados)
            Transcripts/     <-- opcional (.txt por turno de fala)
    """
    print("Starting MSP-PODCAST processing...")

    labels_file = os.path.join(base_dir, "Labels", "labels_consensus.csv")
    if not os.path.exists(labels_file):
        # Fallback: alguns usuários extraem o CSV diretamente na raiz.
        labels_file = os.path.join(base_dir, "labels_consensus.csv")

    if not os.path.exists(labels_file):
        print("Error: 'labels_consensus.csv' not found (esperado em 'Labels/').")
        return None

    print(f"Loading labels from {labels_file}...")
    labels_df = pd.read_csv(labels_file)

    trans_map = load_transcriptions(base_dir)
    audio_root = os.path.join(base_dir, "Audios")

    all_file_data = []

    for _, row in labels_df.iterrows():
        filename = str(row['FileName']).strip()
        if not filename.endswith(".wav"):
            continue

        basename = os.path.splitext(filename)[0]

        # Speaker: numérico no CSV; pode vir como "Unknown".
        raw_spkr = str(row['SpkrID']).strip()
        speaker_id = "Unknown" if raw_spkr == "Unknown" else f"msp_podcast_{raw_spkr}"

        gender = str(row['Gender']).strip()  # Male / Female / Unknown

        emo_code = str(row['EmoClass']).strip()
        emotion = EMOTION_MAP.get(emo_code, emo_code)

        file_info = {
            'dataset': 'MSP-PODCAST',
            'file_path': os.path.join(audio_root, filename),
            'speaker_id': speaker_id,
            'gender': gender,
            'language': 'en',
            'sentence_text': trans_map.get(basename),
            'emotion': emotion,
        }
        all_file_data.append(file_info)

    if not all_file_data:
        return None

    df = pd.DataFrame(all_file_data)

    standard_columns = [
        'dataset', 'file_path', 'speaker_id', 'gender',
        'emotion', 'sentence_text', 'language'
    ]

    for col in standard_columns:
        if col not in df:
            df[col] = pd.NA

    print(f"MSP-PODCAST processing complete. {len(df)} files processed.")
    return df[standard_columns]
