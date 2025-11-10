# tests/test_quality_checks.py
import pandas as pd
from datetime import datetime
from src.bankops.quality_checks import run_quality_checks, STATUS_SET

def _ok_df():
    return pd.DataFrame([
        {"tx_id":"A1","merchant_id":"M1","channel":"WEB","country":"CO","amount":100.0,"status":"APPROVED","tx_timestamp":datetime(2025,1,1,10)},
        {"tx_id":"A2","merchant_id":"M1","channel":"APP","country":"CO","amount":50.0,"status":"DECLINED","tx_timestamp":datetime(2025,1,1,11)},
    ])

def test_quality_pass_basic():
    rep = run_quality_checks(_ok_df())
    assert rep["summary"]["checks_failed"] == 0
    assert rep["summary"]["passed"] is True

def test_bad_status_fails():
    bad = _ok_df().copy()
    bad.loc[0, "status"] = "SOMETHING_ELSE"
    rep = run_quality_checks(bad)
    assert any(c["name"] == "status_domain" and c["status"] == "FAIL" for c in rep["checks"])

def test_dup_tx_id_fails():
    bad = pd.concat([_ok_df(), _ok_df().iloc[[0]]], ignore_index=True)
    rep = run_quality_checks(bad)
    assert any(c["name"] == "unique_tx_id" and c["status"] == "FAIL" for c in rep["checks"])
