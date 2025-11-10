.PHONY: setup synth kpis qc test quality cov clean

setup:
	pip install -r requirements.txt
	pip install -e .[dev]
	pre-commit install

synth:
	python tools/generate_synthetic.py

kpis:
	python -m src.bankops.kpis --input data/processed/transactions_clean.parquet --prefix local

qc:
	python -m src.bankops.quality_checks

test:
	pytest

quality:
	ruff check --fix .
	black .
	mypy src

cov:
	pytest --cov=src --cov-report=term-missing --cov-report=xml:reports/coverage.xml

clean:
	rm -rf reports/*.csv reports/*.png reports/*.json reports/coverage.xml .pytest_cache .mypy_cache
