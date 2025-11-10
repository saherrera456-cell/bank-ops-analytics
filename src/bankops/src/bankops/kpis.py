# src/bankops/kpis.py
import argparse
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[2] if (Path(__file__).resolve().parents[1].name == 'src') else Path.cwd()
DATA_PROCESSED = BASE / "data" / "processed"
REPORTS = BASE / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

CLEAN_PARQUET = DATA_PROCESSED / "transactions_clean.parquet"

APPROVED = "APPROVED"
DECLINED = "DECLINED"
REFUNDED = "REFUNDED"
CHARGEBACK = "CHARGEBACK"

def _rate(numer, denom):
    return float(numer) / float(denom) if denom else 0.0

def _coerce_ts(df):
    if "tx_timestamp" in df.columns:
        df["tx_timestamp"] = pd.to_datetime(df["tx_timestamp"], errors="coerce")
        df["date"] = df["tx_timestamp"].dt.date
        df["hour"] = df["tx_timestamp"].dt.hour
    return df

def load_clean_df(path=CLEAN_PARQUET):
    df = pd.read_parquet(path)
    return _coerce_ts(df)

def kpis_overall(df: pd.DataFrame) -> pd.DataFrame:
    total = len(df)
    n_approved = (df["status"] == APPROVED).sum()
    n_declined = (df["status"] == DECLINED).sum()
    n_refunded = (df["status"] == REFUNDED).sum()
    n_chargeback = (df["status"] == CHARGEBACK).sum()

    out = {
        "total_tx": total,
        "approved_tx": n_approved,
        "declined_tx": n_declined,
        "refunded_tx": n_refunded,
        "chargeback_tx": n_chargeback,
        "approval_rate": _rate(n_approved, total),
        "decline_rate": _rate(n_declined, total),
        "refund_rate": _rate(n_refunded, total),
        "chargeback_rate": _rate(n_chargeback, total),
        "total_amount": float(df["amount"].sum()),
        "avg_ticket": float(df["amount"].mean()) if total else 0.0,
        "median_ticket": float(df["amount"].median()) if total else 0.0,
    }
    return pd.DataFrame([out])

def kpis_by(df: pd.DataFrame, dims=("date",)) -> pd.DataFrame:
    # agrupa por dimensiones y calcula métricas
    g = df.groupby(list(dims), dropna=False)
    res = g.agg(
        total_tx=("tx_id", "count"),
        total_amount=("amount", "sum"),
        approved_tx=("status", lambda s: (s == APPROVED).sum()),
        declined_tx=("status", lambda s: (s == DECLINED).sum()),
        refunded_tx=("status", lambda s: (s == REFUNDED).sum()),
        chargeback_tx=("status", lambda s: (s == CHARGEBACK).sum()),
        avg_ticket=("amount", "mean")
    ).reset_index()
    # tasas
    res["approval_rate"] = res["approved_tx"] / res["total_tx"]
    res["decline_rate"] = res["declined_tx"] / res["total_tx"]
    res["refund_rate"] = res["refunded_tx"] / res["total_tx"]
    res["chargeback_rate"] = res["chargeback_tx"] / res["total_tx"]
    return res

def export_reports(df: pd.DataFrame, prefix="bankops"):
    overall = kpis_overall(df)
    by_date = kpis_by(df, ("date",))
    by_channel = kpis_by(df, ("channel",))
    by_country = kpis_by(df, ("country",))
    by_merchant = kpis_by(df, ("merchant_id",))
    by_hour = kpis_by(df, ("date","hour"))

    overall.to_csv(REPORTS / f"{prefix}_kpi_overall.csv", index=False)
    by_date.to_csv(REPORTS / f"{prefix}_kpi_by_date.csv", index=False)
    by_channel.to_csv(REPORTS / f"{prefix}_kpi_by_channel.csv", index=False)
    by_country.to_csv(REPORTS / f"{prefix}_kpi_by_country.csv", index=False)
    by_merchant.to_csv(REPORTS / f"{prefix}_kpi_by_merchant.csv", index=False)
    by_hour.to_csv(REPORTS / f"{prefix}_kpi_by_hour.csv", index=False)
    return {
        "overall": overall,
        "by_date": by_date,
        "by_channel": by_channel,
        "by_country": by_country,
        "by_merchant": by_merchant,
        "by_hour": by_hour,
    }

def main():
    parser = argparse.ArgumentParser(description="Compute BankOps KPIs and export CSV reports.")
    parser.add_argument("--input", type=str, default=str(CLEAN_PARQUET), help="Path to clean parquet file.")
    parser.add_argument("--prefix", type=str, default="bankops", help="Output file prefix for reports.")
    args = parser.parse_args()

    df = load_clean_df(Path(args.input))
    export_reports(df, prefix=args.prefix)
    print(">> KPIs exported to ./reports")

if __name__ == "__main__":
    main()
