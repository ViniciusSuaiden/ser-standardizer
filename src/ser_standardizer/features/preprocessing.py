import soundfile as sf
import scipy.signal
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

def remove_silence(audio, sr=16000, frame_length=2048, hop_length=512, threshold=0.25):
    audio_clean = nr.reduce_noise(y=audio, sr=sr)

    n_frames = 1 + (len(audio_clean) - frame_length) // hop_length
    if n_frames <= 0:
        return audio_clean

    rms = np.array([
        np.sqrt(np.mean(audio_clean[i*hop_length : i*hop_length + frame_length] ** 2))
        for i in range(n_frames)
    ])

    max_rms = np.max(rms)
    if max_rms == 0:
        return np.array([])

    rms_norm = rms / max_rms
    speech_mask = rms_norm > threshold

    sample_mask = np.zeros(len(audio_clean), dtype=bool)
    for i, active in enumerate(speech_mask):
        if active:
            start = i * hop_length
            end = min(start + hop_length, len(audio_clean))
            sample_mask[start:end] = True

    return audio_clean[sample_mask]

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

