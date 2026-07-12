from .crema_d import process as process_crema
from .iemocap import process as process_iemocap
from .msp_improv import process as process_msp
from .msp_podcast import process as process_msp_podcast
from .emouerj import process as process_emouerj
from .ravdess import process as process_ravdess
from .emodb import process as process_emodb

# Dicionário que mapeia o nome do dataset (string) para a função de processamento
DATASET_LOADERS = {
    'crema_d': process_crema,
    'iemocap': process_iemocap,
    'msp_improv': process_msp,
    'msp_podcast': process_msp_podcast,
    'emouerj': process_emouerj,
    'ravdess': process_ravdess,
    'emodb': process_emodb
}

def get_available_datasets():
    return list(DATASET_LOADERS.keys())