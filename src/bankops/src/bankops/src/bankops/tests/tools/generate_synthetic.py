# tools/generate_synthetic.py
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw"
PROCESSED = BASE / "data" / "processed"
RAW.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)

def main():
    now = datetime(2025, 1, 2, 12, 0, 0)
    rows = []
    for i in range(1, 51):
        rows.append({
            "tx_id": f"T{i:04d}",
            "merchant_id": f"M{(i%5)+1:03d}",
            "channel": ["WEB","APP","POS"][i % 3],
            "country": ["CO","MX","CL"][i % 3],
            "amount": float(10 + (i % 20) * 5),
            "status": ["APPROVED","DECLINED","REFUNDED","CHARGEBACK"][i % 4],
            "tx_timestamp": now - timedelta(hours=i)
        })
    df = pd.DataFrame(rows)
    # Guardar CSV "raw" y Parquet "processed" simplificado
    df.to_csv(RAW / "transactions_sample.csv", index=False)
    df.to_parquet(PROCESSED / "transactions_clean.parquet", index=False)
    print(">> Synthetic data generated under data/raw and data/processed")

if __name__ == "__main__":
    main()
