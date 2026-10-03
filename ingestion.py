import pandas as pd
from datasets import load_dataset
from pathlib import Path

DATASET_NAME = "datahiveai/Amazon-Reviews-Dataset"

SAVE_DIR = Path("data")
SAVE_DIR.mkdir(exist_ok=True)

BASE = "hf://datasets/datahiveai/Amazon-Reviews-Dataset"

for name in ["reviews"]:
    ds = load_dataset("csv", data_files=f"{BASE}/{name}.csv", split="train")
    path = SAVE_DIR / f"{name}.csv"
    ds.to_pandas().to_csv(path, index=False)
    print(f"{name}: {len(ds)} rows -> {path}")