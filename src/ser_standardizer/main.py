import argparse
import os
import pandas as pd
from pathlib import Path
from src.loaders import DATASET_LOADERS, get_available_datasets

def main():
    parser = argparse.ArgumentParser(description="Padronizador de Datasets de Emoção em Fala")
    
    parser.add_argument('--dataset', type=str, required=True, 
                        choices=get_available_datasets(),
                        help='Qual dataset processar')
    
    parser.add_argument('--input_dir', type=str, required=True, 
                        help='Caminho raiz onde o dataset original está salvo')

    args = parser.parse_args()

    if args.dataset not in DATASET_LOADERS:
        print(f"Dataset {args.dataset} não suportado.")
        return

    process_func = DATASET_LOADERS[args.dataset]

    print(f"--- Iniciando padronização do {args.dataset.upper()} ---")
    df = process_func(os.path.abspath(args.input_dir))

    if df is not None and not df.empty:
        DATA_DIR = os.path.join(Path.home(), ".ser_standardizer_data")
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        DATA_FILE = os.path.join(DATA_DIR, f"process_{args.dataset}.csv")
        df.to_csv(DATA_FILE, index=False)
        print(f"Sucesso! CSV salvo em: {DATA_FILE}. Não o renomeie!")
        print(f"Total de amostras: {len(df)}")
    else:
        print("Falha: O DataFrame retornado está vazio ou ocorreu um erro.")

if __name__ == "__main__":
    main()