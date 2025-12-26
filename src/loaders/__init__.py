from .crema_d import process as process_crema
from .iemocap import process as process_iemocap
from .savee import process as process_savee
from .msp_improv import process as process_msp
from .emouerj import process as process_emouerj

# Dicionário que mapeia o nome do dataset (string) para a função de processamento
DATASET_LOADERS = {
    'crema_d': process_crema,
    'iemocap': process_iemocap,
    'savee': process_savee,
    'msp_improv': process_msp,
    'emouerj': process_emouerj
}

def get_available_datasets():
    return list(DATASET_LOADERS.keys())