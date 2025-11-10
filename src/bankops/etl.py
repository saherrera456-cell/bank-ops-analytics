# src/bankops/etl.py
import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

BASE = Path(__file__).resolve().parents[2] if (Path(__file__).resolve().parents[1].name == 'src') else Path.cwd()
DATA_RAW = BASE / "data" / "raw"
DATA_PROCESSED = BASE / "data" / "processed"
DATA_RAW.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

RAW_CSV = DATA_RAW / "transactions_sample.csv"
CLEAN_PARQUET = DATA_PROCESSED / "transactions_clean.parquet"
SQLITE_DB = BASE / "data" / "bank_ops.sqlite"

CHANNELS = ["WEB", "APP", "POS"]
STATUSES = ["APPROVED", "DECLINED", "REFUNDED", "CHARGEBACK"]
MERCHANTS = ["M001", "M002", "M003", "M004", "M005"]
COUNTRIES = ["CO", "MX", "CL", "PE", "AR"]

def _generate_synthetic_csv(n=5000, seed=42):
    rng = np.random.default_rng(seed)
    start = datetime.now() - timedelta(days=60)
    ts = [start + timedelta(minutes=int(rng.integers(0, 60*60))) for _ in range(n)]
    df = pd.DataFrame({
        "tx_id": [f"TX{100000+i}" for i in range(n)],
        "merchant_id": rng.choice(MERCHANTS, size=n, replace=True),
        "channel": rng.choice(CHANNELS, size=n, replace=True, p=[0.45, 0.40, 0.15]),
        "country": rng.choice(COUNTRIES, size=n, replace=True),
        "amount": rng.gamma(shape=2.0, scale=30.0, size=n).round(2),
        "status": rng.choice(STATUSES, size=n, replace=True, p=[0.82, 0.12, 0.04, 0.02]),
        "tx_timestamp": [t.isoformat(timespec="seconds") for t in ts]
    })
    # Introducir algunos nulos y outliers leves para realismo:
    mask_nulls = rng.random(n) < 0.01
    df.loc[mask_nulls, "country"] = None
    df.loc[rng.random(n) < 0.005, "amount"] *= 6  # outliers
    df.to_csv(RAW_CSV, index=False)

def load_raw():
    if not RAW_CSV.exists():
        _generate_synthetic_csv()
    return pd.read_csv(RAW_CSV)

def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Tipos y normalización
    df["tx_timestamp"] = pd.to_datetime(df["tx_timestamp"], errors="coerce")
    df = df.dropna(subset=["tx_timestamp", "amount"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
    # Reglas de dominio
    df["channel"] = df["channel"].str.upper().where(df["channel"].isin(CHANNELS), "WEB")
    df["status"] = df["status"].str.upper().where(df["status"].isin(STATUSES), "DECLINED")
    df["country"] = df["country"].fillna("CO")
    # Cotas razonables de monto
    df = df[(df["amount"] >= 0) & (df["amount"] <= 10000)]
    # Claves
    df = df.drop_duplicates(subset=["tx_id"]).reset_index(drop=True)
    return df

def save_clean(df: pd.DataFrame):
    df.to_parquet(CLEAN_PARQUET, index=False)

def to_sqlite(df: pd.DataFrame):
    import sqlite3
    conn = sqlite3.connect(SQLITE_DB)
    df.to_sql("transactions", conn, if_exists="replace", index=False)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_tx_time ON transactions(tx_timestamp);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_tx_merchant ON transactions(merchant_id);")
    conn.commit()
    conn.close()

def main():
    print(">> ETL start")
    raw = load_raw()
    clean_df = clean(raw)
    save_clean(clean_df)
    to_sqlite(clean_df)
    print(f">> Clean rows: {len(clean_df)}")
    print(">> ETL done")

if __name__ == "__main__":
    main()
