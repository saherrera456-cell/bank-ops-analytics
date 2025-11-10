# src/bankops/quality_checks.py
import json
from pathlib import Path
from datetime import datetime
import pandas as pd

BASE = Path(__file__).resolve().parents[2] if (Path(__file__).resolve().parents[1].name == 'src') else Path.cwd()
DATA_PROCESSED = BASE / "data" / "processed"
REPORTS = BASE / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

CLEAN_PARQUET = DATA_PROCESSED / "transactions_clean.parquet"

EXPECTED_COLS = [
    "tx_id", "merchant_id", "channel", "country",
    "amount", "status", "tx_timestamp"
]
STATUS_SET = {"APPROVED", "DECLINED", "REFUNDED", "CHARGEBACK"}

TIME_MIN = datetime(2018, 1, 1)
TIME_MAX = datetime(2030, 12, 31)
AMOUNT_MIN = 0.0
AMOUNT_MAX = 100000.0

def _load_df(path=CLEAN_PARQUET) -> pd.DataFrame:
    df = pd.read_parquet(path)
    if "tx_timestamp" in df.columns:
        df["tx_timestamp"] = pd.to_datetime(df["tx_timestamp"], errors="coerce", utc=False)
    return df

def _fail_export(df: pd.DataFrame, name: str):
    if df is None or df.empty:
        return None
    path = REPORTS / f"qc_fail_{name}.csv"
    df.to_csv(path, index=False)
    return str(path)

def run_quality_checks(df: pd.DataFrame) -> dict:
    report = {"checks": [], "summary": {}}

    # 1) Esquema
    missing = [c for c in EXPECTED_COLS if c not in df.columns]
    extra = [c for c in df.columns if c not in EXPECTED_COLS]
    report["checks"].append({
        "name": "schema_columns",
        "status": "PASS" if not missing else "FAIL",
        "missing_columns": missing,
        "extra_columns": extra
    })

    # 2) Nulos clave
    null_keys = df[df["tx_id"].isna()]
    null_ts = df[df["tx_timestamp"].isna()]
    null_status = df[df["status"].isna()]
    report["checks"].append({
        "name": "not_null_keys",
        "status": "PASS" if null_keys.empty else "FAIL",
        "failed_rows_csv": _fail_export(null_keys, "null_tx_id")
    })
    report["checks"].append({
        "name": "not_null_timestamp",
        "status": "PASS" if null_ts.empty else "FAIL",
        "failed_rows_csv": _fail_export(null_ts, "null_timestamp")
    })
    report["checks"].append({
        "name": "not_null_status",
        "status": "PASS" if null_status.empty else "FAIL",
        "failed_rows_csv": _fail_export(null_status, "null_status")
    })

    # 3) Dominio de status
    bad_status = df[~df["status"].isin(STATUS_SET)]
    report["checks"].append({
        "name": "status_domain",
        "status": "PASS" if bad_status.empty else "FAIL",
        "allowed": sorted(list(STATUS_SET)),
        "failed_rows_csv": _fail_export(bad_status, "bad_status")
    })

    # 4) Duplicados por tx_id
    dups = df[df.duplicated(subset=["tx_id"], keep=False)]
    report["checks"].append({
        "name": "unique_tx_id",
        "status": "PASS" if dups.empty else "FAIL",
        "failed_rows_csv": _fail_export(dups, "duplicate_tx_id")
    })

    # 5) Rango de montos
    bad_amt = df[(df["amount"] < AMOUNT_MIN) | (df["amount"] > AMOUNT_MAX) | (df["amount"].isna())]
    report["checks"].append({
        "name": "amount_range",
        "status": "PASS" if bad_amt.empty else "FAIL",
        "range": [AMOUNT_MIN, AMOUNT_MAX],
        "failed_rows_csv": _fail_export(bad_amt, "amount_range")
    })

    # 6) Ventana temporal
    bad_time = df[(df["tx_timestamp"] < TIME_MIN) | (df["tx_timestamp"] > TIME_MAX) | (df["tx_timestamp"].isna())]
    report["checks"].append({
        "name": "timestamp_window",
        "status": "PASS" if bad_time.empty else "FAIL",
        "window": [TIME_MIN.isoformat(), TIME_MAX.isoformat()],
        "failed_rows_csv": _fail_export(bad_time, "timestamp_window")
    })

    # Resumen rápido
    total = len(df)
    n_fail = sum(1 for c in report["checks"] if c["status"] == "FAIL")
    report["summary"] = {
        "rows_evaluated": total,
        "checks_total": len(report["checks"]),
        "checks_failed": n_fail,
        "passed": n_fail == 0
    }

    with open(REPORTS / "quality_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)
    return report

def main():
    df = _load_df(CLEAN_PARQUET)
    rep = run_quality_checks(df)
    # Mensaje breve en CI
    status = "PASS" if rep["summary"]["passed"] else "FAIL"
    print(f">> QUALITY: {status} | checks_failed={rep['summary']['checks_failed']}")

if __name__ == "__main__":
    main()
