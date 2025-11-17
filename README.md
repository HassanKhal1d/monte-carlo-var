# Monte Carlo VaR Model
Monte Carlo VaR engine for S&amp;P 500 (GBM + Merton jump-diffusion) with interactive React UI, backtest &amp; K–S goodness-of-fit.
## Quickstart

### Backend
```bash
cd backend/app
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
python data_fetch.py       # downloads data to backend/app/data/spy.csv
uvicorn main:app --reload --port 8000

cd frontend
npm install
npm run dev

---

## 3) Backend files (create under `backend/app/`)

#### `__init__.py`
```python
# backend/app/__init__.py
# Empty - required to make this folder a Python package.

