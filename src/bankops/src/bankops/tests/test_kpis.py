# tests/test_kpis.py
import pandas as pd
from datetime import datetime
from src.bankops.kpis import kpis_overall, kpis_by, _coerce_ts

def _mini_df():
    data = [
        {"tx_id":"T1","merchant_id":"M001","channel":"WEB","country":"CO","amount":100.0,"status":"APPROVED","tx_timestamp":datetime(2025,1,1,10,0,0)},
        {"tx_id":"T2","merchant_id":"M001","channel":"APP","country":"CO","amount":50.0,"status":"DECLINED","tx_timestamp":datetime(2025,1,1,11,0,0)},
        {"tx_id":"T3","merchant_id":"M002","channel":"WEB","country":"MX","amount":75.0,"status":"APPROVED","tx_timestamp":datetime(2025,1,1,12,0,0)},
        {"tx_id":"T4","merchant_id":"M002","channel":"POS","country":"CO","amount":25.0,"status":"REFUNDED","tx_timestamp":datetime(2025,1,2,13,0,0)},
        {"tx_id":"T5","merchant_id":"M003","channel":"APP","country":"CL","amount":10.0,"status":"CHARGEBACK","tx_timestamp":datetime(2025,1,2,14,0,0)},
    ]
    return _coerce_ts(pd.DataFrame(data))

def test_overall_kpis_sum():
    df = _mini_df()
    overall = kpis_overall(df).iloc[0]
    assert overall["total_tx"] == 5
    assert overall["approved_tx"] == 2
    assert overall["declined_tx"] == 1
    assert overall["refunded_tx"] == 1
    assert overall["chargeback_tx"] == 1
    # tasas
    assert abs(overall["approval_rate"] - 0.4) < 1e-9
    assert abs(overall["decline_rate"] - 0.2) < 1e-9

def test_group_by_date():
    df = _mini_df()
    by_date = kpis_by(df, ("date",))
    totals = by_date.set_index("date")["total_tx"].to_dict()
    # 2025-01-01 tiene 3, 2025-01-02 tiene 2
    assert sum(totals.values()) == 5
    assert min(totals.values()) == 2
    assert max(totals.values()) == 3
