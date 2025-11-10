from pathlib import Path
import duckdb

BASE = Path(__file__).resolve().parents[2]
DB = BASE / "data" / "bankops.duckdb"
DB.parent.mkdir(parents=True, exist_ok=True)

def get_connection():
    return duckdb.connect(str(DB))

def load_parquet_to_duckdb(parquet_path: Path, table: str = "transactions"):
    con = get_connection()
    con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM parquet_scan('{parquet_path}');")
    con.close()
