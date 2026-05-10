import soundfile as sf
import scipy.signal
from scipy.ndimage import maximum_filter1d
import numpy as np
from IPython.display import Audio, display
from tqdm.auto import tqdm
import noisereduce as nr

def scipy_load(path, target_sr=None):

    audio, native_sr = sf.read(path)
    
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)
        
    if target_sr is not None and native_sr != target_sr:
        num_samples = round(len(audio) * float(target_sr) / native_sr)
        audio = scipy.signal.resample(audio, num_samples)
        return audio, target_sr
        
    return audio, native_sr

def split_silence(audio, top_db=60, frame_length=2048):
    max_amplitude = np.max(np.abs(audio))
    if max_amplitude == 0:
        return np.array([[0, len(audio)]])
    
    threshold_linear = max_amplitude * (10 ** (-top_db / 20))
    
    envelope = maximum_filter1d(np.abs(audio), size=frame_length)
    
    active_mask = envelope > threshold_linear
    
    edges = np.diff(active_mask.astype(int))
    starts = np.where(edges == 1)[0]
    ends = np.where(edges == -1)[0]
    
    if active_mask[0]:
        starts = np.insert(starts, 0, 0)
    if active_mask[-1]:
        ends = np.append(ends, len(audio))
        
    return np.column_stack((starts, ends))

def remove_silence(audio, sr=16000, top_db=30):
    """
    Aplica redução de ruído e remove silêncios baseados em energia.
    Retorna o vetor NumPy contendo apenas a fonação efetiva.
    """
    audio_clean = nr.reduce_noise(y=audio, sr=sr)
    intervals = split_silence(audio_clean, top_db=top_db)
    
    if len(intervals) > 0:
        audio_no_silence = np.concatenate([audio_clean[start:end] for start, end in intervals])
        return audio_no_silence
    else:
        return np.array([])

def listen(df, index):
    if index not in df.index:
        print(f"Aviso: Não há nenhum áudio disponível com o índice {index}.")
        return

    path = df.loc[index, 'file_path']
    emotion = df.loc[index, 'emotion']
    
    print(f"Tocando áudio {index} | Emoção: {emotion}")
    display(Audio(filename=path))

def load_audio(df, index, sr=16000):
    if index not in df.index:
        raise IndexError("Índice não encontrado no Dataset.")
    path = df.loc[index, 'file_path']
    audio, _ = scipy_load(path, target_sr=sr)
    return audio

def load_batch(df, begin, end, sr=16000, max_1000=True):
    qtd = end - begin
    if qtd > 1000 and max_1000:
        raise ValueError(f"Você tentou carregar {qtd} áudios. O limite é 1000. Defina max_1000=False se tiver certeza.")

    batch = []
    subset_indices = df.index[begin:end]

    for idx in tqdm(subset_indices, desc="Carregando áudios"):
        try:
            audio = load_audio(df, idx, sr)
            batch.append(audio)
        except Exception as e:
            print(f"Erro ao carregar índice {idx}: {e}")
            batch.append(None)

    max_len = max(len(x) for x in batch if x is not None)
    padded_batch = np.zeros((len(batch), max_len), dtype=np.float32)

    for i, audio in enumerate(batch):
        if audio is not None:
            padded_batch[i, :audio.shape[0]] = audio
            
    return padded_batch

def mean_energy(audio, sr=16000, top_db=30):
    """
    Aplica redução de ruído, remove silêncios e extrai a energia média (Mean Square).
    """
    audio_clean = nr.reduce_noise(y=audio, sr=sr)

    intervals = split_silence(audio_clean, top_db=top_db)
    
    if len(intervals) > 0:
        audio_no_silence = np.concatenate([audio_clean[start:end] for start, end in intervals])
    else:
        audio_no_silence = np.array([])

    if len(audio_no_silence) == 0:
        return 0.0

    energy = np.mean(audio_no_silence ** 2)
    
    return float(energy)