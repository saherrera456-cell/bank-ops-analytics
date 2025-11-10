# Bank Ops Analytics — Payments, Risk & Operational Insights

**Purpose:** End-to-end analytics project for banking/fintech roles (Business Analyst, Data Analyst, Risk/Operations Analyst). It demonstrates data cleaning, SQL KPIs, Python analytics, operational/risk insights, dashboards, testing and CI—using synthetic, privacy-safe data.

---

## Highlights
- **Business-first**: KPIs and insights aligned to real banking ops (approval rate, losses, SLA, backlog, risk flags).
- **Technical depth**: Python (pandas), SQL (SQLite), tests (pytest), CI (GitHub Actions), clean repo structure.
- **Storytelling**: clear README, glossary, and recommendations for decision-makers.

---

## Objectives
1) Transform raw financial-like events into decision-ready KPIs.  
2) Build reproducible ETL + analytics with Python & SQL.  
3) Communicate risk/ops opportunities via documentation & dashboard.  
4) Show good engineering habits (testing, CI, structure, versioning).

---

## Repository Structure
bank-ops-analytics/
├─ README.md
├─ LICENSE
├─ .gitignore
├─ requirements.txt
├─ data/
│ ├─ raw/transactions_sample.csv # synthetic sample
│ └─ processed/transactions_clean.parquet
├─ sql/
│ ├─ create_tables.sql
│ └─ analytics_queries.sql
├─ src/bankops/
│ ├─ init.py
│ ├─ etl.py # load → clean → save
│ ├─ kpis.py # KPIs & summaries
│ └─ utils.py
├─ tests/
│ └─ test_kpis.py # unit tests for KPIs
├─ notebooks/
│ └─ 00_EDA_outline.md # EDA guide (optional Jupyter)
├─ dashboards/
│ └─ README.md # Power BI/Streamlit notes
├─ docs/
│ └─ glossary.md # KPI definitions & assumptions
└─ .github/workflows/
└─ ci.yml # flake8 + pytest

---

## 🛠️ Stack
- **Python**: pandas, numpy, pytest, flake8  
- **SQL**: SQLite (portable & easy to reproduce)  
- **Dashboards**: Power BI / Streamlit (optional)  
- **CI/CD**: GitHub Actions (lint + tests)

Install:
    
    python -m venv .venv && source .venv/bin/activate     # Win: .venv\Scripts\activate
    pip install -r requirements.txt

Run ETL and KPIs:
    
    python -m src.bankops.etl
    python -m src.bankops.kpis

Run tests & lint:
    
    pytest -q
    flake8 src

---

## 📊 Core Banking/Operations KPIs
| KPI | Descripción | Fórmula (conceptual) |
| --- | --- | --- |
| Approval Rate | % de transacciones aprobadas | approved / total |
| Loss Amount | Pérdidas por chargeback+refund | Σ amount (status ∈ {CHARGEBACK, REFUNDED}) |
| Tx Volume by Channel | Volumen y valor por canal (WEB/APP/POS) | group by channel |
| Merchant Risk Snapshot | Merchants con mayor pérdida/incidencia | rank(loss, disputes) |
| Backlog/Aging (ops) | Pendientes por severidad/tiempo | buckets por SLA (opcional) |

SQL examples (`sql/analytics_queries.sql`):

- Approval rate por día:
    
        SELECT DATE(tx_timestamp) d,
               100.0 * AVG(CASE WHEN status='APPROVED' THEN 1 ELSE 0 END) AS approval_rate
        FROM transactions
        GROUP BY 1
        ORDER BY 1;

- Pérdida por tipo:
    
        SELECT status, SUM(amount) total_amount
        FROM transactions
        WHERE status IN ('CHARGEBACK','REFUNDED')
        GROUP BY status;

---

## 🔍 Process Overview
1) **Ingest**: `transactions_sample.csv` (sintético) → ETL en `src/bankops/etl.py`.  
2) **Clean**: tipificación, normalización, nulos, dominios.  
3) **Store**: parquet limpio en `data/processed/`.  
4) **Analyze**: KPIs con `src/bankops/kpis.py` + SQL de `sql/`.  
5) **Communicate**: dashboard (opcional) + `docs/glossary.md` + README.  
6) **Quality**: tests (`tests/`) + CI (`.github/workflows/ci.yml`).  

---

##  Example Insights 
- Approval rate estable >82%, caída puntual en POS horas pico (riesgo de capacidad).  
- 78% de pérdidas concentradas en 2 merchants; priorizar revisión contractual/monitoring.  
- Web tiene menor pérdida relativa que POS, pero mayor dispersión por ticket medio (ojo con límites/monitoring).  

---

## Dashboard 
- KPIs: Approval, Loss, Volume, Top Merchants, Canal x País.  
- Filtros por ventana temporal, canal, merchant.  
- Export de “Executive Snapshot” mensual para stakeholders.

Ver `dashboards/README.md` para instrucciones.

---

## Testing & CI
- `pytest`: valida funciones de KPI.  
- `flake8`: estilo y calidad.  
- GitHub Actions (`ci.yml`): ejecuta lint+tests en cada push/PR.

---

## Data & Ethics
- Dataset **sintético** sin PII.  
- Diseñado para educación/portafolio.  
- Acepta ampliación con datos públicos debidamente anonimizados.

---

## License
MIT — ver `LICENSE`.

---

##  Contact
- **Name**: Santiago Herrera Rojas — Bogotá, Colombia  
- **Email**: saherrera456@gmail.com  
- **LinkedIn**: https://www.linkedin.com/in/santiago-herrera-rojas-0b6985131

> This repository is part of a professional portfolio oriented to banking/fintech analytics and operational excellence.
