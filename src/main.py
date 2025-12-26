import argparse
import os
import pandas as pd
from src.loaders import DATASET_LOADERS, get_available_datasets

def main():
    parser = argparse.ArgumentParser(description="Padronizador de Datasets de Emoção em Fala")
    
    parser.add_argument('--dataset', type=str, required=True, 
                        choices=get_available_datasets(),
                        help='Qual dataset processar')
    
    parser.add_argument('--input_dir', type=str, required=False, 
                        help='Caminho raiz onde o dataset original está salvo')
    
    parser.add_argument('--output_csv', type=str, required=True, 
                        help='Caminho onde salvar o CSV padronizado final')

    args = parser.parse_args()

    if args.dataset not in DATASET_LOADERS:
        print(f"Dataset {args.dataset} não suportado.")
        return

    process_func = DATASET_LOADERS[args.dataset]

    print(f"--- Iniciando padronização do {args.dataset.upper()} ---")
    df = process_func(args.input_dir)

    if df is not None and not df.empty:
        output_csv = os.path.abspath(args.output_csv)
        if os.path.isdir(output_csv):
            os.makedirs(os.path.dirname(output_csv), exist_ok=True)
            df.to_csv(os.path.join(output_csv, "standardized_" + args.dataset + ".csv"), index=False)
        else:
            df.to_csv(output_csv, index=False)
        print(f"Sucesso! CSV salvo em: {args.output_csv}")
        print(f"Total de amostras: {len(df)}")
    else:
        print("Falha: O DataFrame retornado está vazio ou ocorreu um erro.")

if __name__ == "__main__":
    main()