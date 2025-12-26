import os
import pandas as pd

# --- MAPS ---
EMOTION_MAP = {
    'A': 'Anger', 'H': 'Happy', 'S': 'Sad', 'N': 'Neutral',
    'O': 'Other', 'D': 'Disgust', 'F': 'Fear', 'U': 'Surprise', 'X': 'Unknown'
}

# --- HELPERS ---

def load_evaluations(base_dir):
    """
    Parses Evaluation.txt.
    Normalizes all keys to start with 'MSP-' so they match the audio filenames.
    """
    eval_map = {}
    eval_file = os.path.join(base_dir, "Evaluation.txt")
    
    if not os.path.exists(eval_file):
        print("Warning: Evaluation.txt not found.")
        return eval_map

    print(f"Loading evaluations from {eval_file}...")
    try:
        with open(eval_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('%'): continue
                
                parts = line.split(';')
                first_token = parts[0].strip()
                
                # Only read Master Lines (.avi)
                if not first_token.endswith('.avi'):
                    continue
                
                # Get the base filename without extension
                raw_key = os.path.splitext(first_token)[0]
            
                # "UTD-IMPROV..." -> "MSP" + "-IMPROV..."
                normalized_key = "MSP" + raw_key[3:]
                
                if len(parts) >= 2:
                    raw_emo = parts[1].strip()
                    eval_map[normalized_key] = EMOTION_MAP.get(raw_emo, raw_emo)
                    
    except Exception as e:
        print(f"Error reading Evaluation.txt: {e}")
        
    return eval_map

def load_transcriptions(base_dir):
    """
    Attempts to load transcriptions from 'Human_transcriptions' folder if available.
    Returns { 'filename_no_ext': 'text' }
    """
    trans_map = {}
    trans_dir = os.path.join(base_dir, "All_human_transcriptions")
    
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
    print("Starting MSP-IMPROV processing...")
    
    eval_map = load_evaluations(base_dir)
    trans_map = load_transcriptions(base_dir)
    
    audio_root = os.path.join(base_dir, "Audio")
    if not os.path.exists(audio_root):
        print(f"Error: 'Audio' folder not found.")
        return None

    all_file_data = []

    print(f"Scanning audio files in {audio_root}...")
    for root, _, files in os.walk(audio_root):
        for filename in files:
            if filename.endswith(".wav"):
                basename = os.path.splitext(filename)[0]
                full_path = os.path.join(root, filename)
                parts = basename.split('-')
                
                if len(parts) < 6: continue 
                
                try:
                    # Parsing Metadata
                    sentence_token = parts[2]   # S01A
                    interaction_id = parts[3]   # M01
                    scenario_token = parts[4]   # P, R, S, T
                    turn_token = parts[5]       # FM01
                    
                    sentence_id = sentence_token[:3]
                    intended_emo_code = sentence_token[3]
                    
                    # Speaker
                    speaker_char = turn_token[1] if len(turn_token) >= 2 else 'X'
                    gender = 'Male' if speaker_char == 'M' else 'Female' if speaker_char == 'F' else 'Unknown'
                    speaker_id = f"msp_{interaction_id}_{speaker_char}"

                    # --- Text Logic ---
                    text = trans_map.get(basename)

                    file_info = {
                        'dataset': 'MSP-IMPROV',
                        'file_path': full_path,
                        # 'filename': filename,
                        'speaker_id': speaker_id,
                        'gender': gender,
                        'language': 'en',
                        'sentence_text': text,
                        'emotion': eval_map.get(basename, pd.NA),
                    }
                    all_file_data.append(file_info)

                except Exception as e:
                    print(f"Skipping {filename}: {e}")
                    continue

    if not all_file_data: return None

    df = pd.DataFrame(all_file_data)
    
    standard_columns = [
        'dataset', 'file_path', 'speaker_id', 'gender',
        'emotion', 'sentence_text', 'language'
    ]
    
    for col in standard_columns:
        if col not in df: df[col] = pd.NA
            
    print(f"MSP-IMPROV processing complete. {len(df)} files processed.")
    return df[standard_columns]