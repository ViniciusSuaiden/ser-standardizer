#!/usr/bin/env python3
"""
Pipeline incremental de extração de features para o estudo cross-corpus.

Ideia central: o áudio é grande (GBs), mas as features eGeMAPS são minúsculas
(88 floats por utterance). Então processamos UM corpus por vez, guardamos só a
matriz de features em disco e (opcionalmente) apagamos o áudio bruto antes de
seguir para o próximo. O pico de disco passa a ser o maior corpus isolado, e não
a soma de todos.

Para cada corpus, os 5 passos são:
  1. baixar o corpus            -> pré-requisito MANUAL (veja docs/datasets/)
  2. padronizar os metadados    -> DATASET_LOADERS[name](input_dir)
  3. extrair features (openSMILE) e salvar em parquet/csv
  4. apagar o áudio bruto       -> opcional, via --delete-audio
  5. próximo corpus

No fim você terá um arquivo `features_{dataset}.parquet` por corpus (metadados +
88 features), prontos para o `normalize` + t-SNE da análise cross-corpus.

Uso:
    # edite o CONFIG abaixo com os caminhos dos seus downloads, então:
    python scripts/build_features.py                 # todos os configurados
    python scripts/build_features.py --only crema_d ravdess
    python scripts/build_features.py --cap 300        # 300 por emoção/corpus
    python scripts/build_features.py --delete-audio   # libera o áudio após extrair

Requer a instalação completa:  pip install ".[features]"
"""

import argparse
import shutil
from pathlib import Path

import pandas as pd

from ser_standardizer.loaders import DATASET_LOADERS
from ser_standardizer import extract_features


# --------------------------------------------------------------------------- #
# CONFIGURAÇÃO — ajuste os caminhos para os seus downloads.
# Use None para corpora gerenciados automaticamente (EmoUERJ via audb).
# Comente/remova as linhas dos corpora que ainda não vai processar.
# --------------------------------------------------------------------------- #
CONFIG = {
    "crema_d":     r"/caminho/para/CREMA-D",
    "ravdess":     r"/caminho/para/RAVDESS",
    "emodb":       r"/caminho/para/EmoDB",
    "emouerj":     None,                       # audb baixa e faz cache sozinho
    "iemocap":     r"/caminho/para/IEMOCAP",
    "msp_improv":  r"/caminho/para/MSP-IMPROV",
    "msp_podcast": r"/caminho/para/MSP-PODCAST",   # use uma partição/subset!
}

# As 4 emoções comuns a TODOS os 7 corpora (interseção das taxonomias).
SHARED_EMOTIONS = ["Anger", "Happy", "Sad", "Neutral"]

# Onde salvar as matrizes de features (pequenas — pode versionar/backup).
OUT_DIR = Path.home() / ".ser_standardizer_data" / "features"

# Amostragem por (corpus, emoção). Mantém a figura balanceada e barata.
DEFAULT_CAP = 200
SEED = 42


def standardize(name: str, input_dir):
    """Passo 2 — roda o loader do corpus e devolve o DataFrame padronizado."""
    loader = DATASET_LOADERS[name]
    df = loader(input_dir) if input_dir is not None else loader()
    if df is None or df.empty:
        raise RuntimeError(f"loader de '{name}' retornou vazio — confira o input_dir")
    return df


def subsample(df: pd.DataFrame, cap: int, gender=None, seed: int = SEED):
    """Filtra as 4 emoções comuns (+ gênero opcional) e limita por classe."""
    sub = df[df["emotion"].isin(SHARED_EMOTIONS)]
    if gender is not None:
        sub = sub[sub["gender"].str.lower() == gender.lower()]
    if sub.empty:
        return sub
    sub = sub.groupby("emotion", group_keys=False).apply(
        lambda g: g.sample(min(len(g), cap), random_state=seed)
    )
    return sub.reset_index(drop=True)


def save_features(name: str, meta: pd.DataFrame, feats: pd.DataFrame) -> Path:
    """Passo 3 (persistência) — junta metadados + features e grava em disco."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    combined = pd.concat(
        [meta.reset_index(drop=True), feats.reset_index(drop=True)], axis=1
    )
    out = OUT_DIR / f"features_{name}.parquet"
    try:
        combined.to_parquet(out, index=False)
    except Exception as exc:  # pyarrow/fastparquet ausente
        out = OUT_DIR / f"features_{name}.csv"
        combined.to_csv(out, index=False)
        print(f"   (parquet indisponível: {exc} -> salvo como CSV)")
    return out


def delete_audio(input_dir):
    """Passo 4 — apaga o áudio bruto do corpus (destrutivo; opt-in)."""
    if not input_dir:
        print("   [skip] corpus gerenciado (sem input_dir local para apagar)")
        return
    path = Path(input_dir)
    if not path.exists():
        print(f"   [skip] {path} não existe")
        return
    print(f"   ⚠️  apagando áudio bruto em {path} ...")
    shutil.rmtree(path)


def process_one(name: str, input_dir, cap: int, gender, do_delete: bool):
    print(f"\n=== {name} ===")
    print("[2/4] padronizando metadados...")
    df = standardize(name, input_dir)

    print(f"[2/4] subamostrando (<= {cap}/emoção, emoções={SHARED_EMOTIONS}"
          f"{', gênero=' + gender if gender else ''})...")
    sub = subsample(df, cap=cap, gender=gender)
    if sub.empty:
        print("   [skip] nenhuma amostra após o filtro — pulando corpus")
        return None
    print(f"   {len(sub)} utterances selecionadas")

    print("[3/4] extraindo eGeMAPS (functionals)...")
    feats = extract_features(
        sub, feature_set="eGeMAPS", feature_level="functionals",
        use_vad=False, sr=16000,
    )
    out = save_features(name, sub, feats)
    print(f"[3/4] salvo em {out}  ({feats.shape[1]} features)")

    if do_delete:
        print("[4/4] liberando espaço...")
        delete_audio(input_dir)
    else:
        print("[4/4] --delete-audio não informado; áudio preservado")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", nargs="+", metavar="DATASET",
                    help="processa apenas estes corpora (padrão: todos do CONFIG)")
    ap.add_argument("--cap", type=int, default=DEFAULT_CAP,
                    help=f"máximo de utterances por emoção/corpus (padrão {DEFAULT_CAP})")
    ap.add_argument("--gender", choices=["Male", "Female"], default=None,
                    help="filtra por gênero (padrão: ambos)")
    ap.add_argument("--delete-audio", action="store_true",
                    help="APAGA o áudio bruto (input_dir) após extrair as features")
    args = ap.parse_args()

    targets = args.only or list(CONFIG.keys())
    unknown = [t for t in targets if t not in CONFIG]
    if unknown:
        ap.error(f"corpora não configurados: {unknown}. Disponíveis: {list(CONFIG)}")

    done, failed = [], []
    for name in targets:
        try:
            out = process_one(name, CONFIG[name], args.cap, args.gender, args.delete_audio)
            if out is not None:
                done.append(name)
        except Exception as exc:
            print(f"   [ERRO] {name}: {exc}")
            failed.append(name)

    print("\n--- resumo ---")
    print(f"ok:     {done}")
    print(f"falhou: {failed}")
    print(f"features em: {OUT_DIR}")


if __name__ == "__main__":
    main()
