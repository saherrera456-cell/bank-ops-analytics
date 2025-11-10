from pathlib import Path
from src.bankops.db import get_connection, load_parquet_to_duckdb

BASE = Path(__file__).resolve().parents[1]
PARQ = BASE / "data" / "processed" / "transactions_clean.parquet"
SQL_DIR = BASE / "sql"

def main():
    load_parquet_to_duckdb(PARQ, "transactions")
    con = get_connection()
    for sql_file in ["analytics_queries.sql"]:
        sql_path = SQL_DIR / sql_file
        print(f"\n>> Running: {sql_file}")
        with open(sql_path, "r", encoding="utf-8") as f:
            statements = f.read().strip().split(";")
            for st in statements:
                st = st.strip()
                if not st:
                    continue
                res = con.execute(st).df()
                print(res.head())
    con.close()

if __name__ == "__main__":
    main()
