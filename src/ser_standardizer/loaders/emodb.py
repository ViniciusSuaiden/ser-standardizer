import os
import pandas as pd

# EmoDB (Berlin Database of Emotional Speech) — alemão.
# Formato do nome do arquivo: SSTTTEV.wav
#   SS  -> número do locutor (2 dígitos)
#   TTT -> código do texto (ex.: a01, b03)
#   E   -> letra da emoção (alemão)
#   V   -> versão (a, b, c, ...) quando há mais de uma gravação

# Letras de emoção (iniciais em alemão) mapeadas para o rótulo padrão do repo.
#   W = Wut (raiva), L = Langeweile (tédio), E = Ekel (nojo),
#   A = Angst (medo), F = Freude (alegria), T = Trauer (tristeza), N = Neutral
EMOTION_MAP = {
    'W': 'Anger',
    'L': 'Boredom',
    'E': 'Disgust',
    'A': 'Fear',
    'F': 'Happy',
    'T': 'Sad',
    'N': 'Neutral',
}

# Gênero de cada um dos 10 locutores (conforme documentação oficial do EmoDB).
SPEAKER_GENDER = {
    '03': 'Male',
    '08': 'Female',
    '09': 'Female',
    '10': 'Male',
    '11': 'Male',
    '12': 'Male',
    '13': 'Female',
    '14': 'Female',
    '15': 'Male',
    '16': 'Female',
}

# Frases em alemão associadas a cada código de texto.
SENTENCE_MAP = {
    'a01': "Der Lappen liegt auf dem Eisschrank.",
    'a02': "Das will sie am Mittwoch abgeben.",
    'a04': "Heute abend könnte ich es ihm sagen.",
    'a05': "Das schwarze Stück Papier befindet sich da oben neben dem Holzstück.",
    'a07': "In sieben Stunden wird es soweit sein.",
    'b01': "Was sind denn das für Tüten, die da unter dem Tisch stehen?",
    'b02': "Sie haben es gerade hochgetragen und jetzt gehen sie wieder runter.",
    'b03': "An den Wochenenden bin ich jetzt immer nach Hause gefahren und habe Agnes besucht.",
    'b09': "Ich will das eben wegbringen und dann mit Karl was trinken gehen.",
    'b10': "Die wird auf dem Platz sein, wo wir sie immer hinlegen.",
}


def process(base_dir):
    """
    Processa o dataset EmoDB (Berlin Database of Emotional Speech).

    A estrutura esperada é uma pasta raiz contendo os arquivos .wav
    (as pastas oficiais EmoDB_1/ e EmoDB_2/ podem ser extraídas dentro dela;
    a busca é recursiva).

    Args:
        base_dir (str): Caminho raiz onde os .wav do EmoDB estão salvos.

    Returns:
        pandas.DataFrame: DataFrame padronizado ou None se nada for encontrado.
    """
    print("Iniciando processamento do EmoDB...")

    all_file_data = []

    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            if not filename.lower().endswith('.wav'):
                continue

            file_key = os.path.splitext(filename)[0]

            # Nome padrão do EmoDB tem 7 caracteres: SS TTT E V
            if len(file_key) != 7:
                print(f"Nome fora do padrão, ignorado: {filename}")
                continue

            speaker_id = file_key[0:2]
            text_code = file_key[2:5]
            emotion_code = file_key[5]
            # file_key[6] é a versão, não usada no schema padrão.

            emotion = EMOTION_MAP.get(emotion_code)
            if emotion is None:
                print(f"Emoção desconhecida ({emotion_code}) em {filename}, ignorado.")
                continue

            file_info = {
                'dataset': 'EmoDB',
                'file_path': os.path.join(root, filename),
                'speaker_id': f"emodb_{speaker_id}",
                'gender': SPEAKER_GENDER.get(speaker_id, pd.NA),
                'language': 'de',
                'emotion': emotion,
                'sentence_text': SENTENCE_MAP.get(text_code, "Unknown"),
            }

            all_file_data.append(file_info)

    print(f"Processamento do EmoDB concluído. {len(all_file_data)} arquivos processados.")

    if not all_file_data:
        return None

    final_df = pd.DataFrame(all_file_data)

    standard_columns = [
        'dataset', 'file_path', 'speaker_id', 'gender',
        'emotion', 'sentence_text', 'language'
    ]

    for col in standard_columns:
        if col not in final_df:
            final_df[col] = pd.NA

    return final_df[standard_columns]
