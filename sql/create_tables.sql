-- Base simple
CREATE TABLE IF NOT EXISTS transactions AS
SELECT * FROM read_parquet('data/processed/transactions_clean.parquet');

-- Índices lógicos (DuckDB usa optimizador columnar)

