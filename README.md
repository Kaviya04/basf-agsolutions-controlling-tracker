# BASF SE — Financial Performance & Controlling Review

A one-page controlling analysis of BASF SE's standalone financial statements (FY2008–FY2025), built to show the kind of output an operational/strategic controlling function actually produces: a trend view, a year-over-year P&L bridge, and a balance sheet strength read — each with a short written interpretation, not just a chart.

**Live version:** `https://<your-username>.github.io/basf-controlling-review/`

## Why this exists

This was built as a work sample for BASF's *START IN Finance & Controlling* trainee programme (Controlling track). Rather than a generic finance dashboard, it uses BASF SE's own reported line items — revenue, cost of revenue, SG&A, R&D, EBIT, EBITDA, balance sheet structure — and reads them the way a controller would: what moved, by how much, and why it matters for the business.

## What it shows

1. **Revenue & margin trend (2008–2025)** — how EBIT and EBITDA margin have moved independently of the revenue cycle.
2. **FY2025 P&L bridge** — a line-item waterfall from FY2024 to FY2025, isolating how much of the EBIT change came from cost discipline (SG&A, R&D) versus gross margin pressure.
3. **Balance sheet strength** — equity ratio and net debt/EBITDA trends, read alongside the P&L story to show the leverage trade-off behind the margin recovery.

## Data & methodology

- Source: BASF SE standalone income statement and balance sheet, FY2008–FY2025, EUR (`data/income_basf_se.csv`, `data/balance_basf_se.csv`).
- All figures are taken directly from reported line items — no estimates, no restatements.
- Derived ratios (`data/build_data.py`):
  - Equity ratio = Total Equity / Total Assets
  - Net debt = Short-term Debt + Long-term Debt − Cash & Cash Equivalents
  - Net debt/EBITDA = Net debt / EBITDA
  - Working capital = Inventory + Net Receivables − Accounts Payable

To regenerate `data/data.json` from the source CSVs:

```bash
cd data
python3 build_data.py
```

## Stack

Plain HTML/CSS/JS, [Chart.js](https://www.chartjs.org/) for the trend and ratio charts, no build step, no backend. Data is embedded directly in `index.html` so it runs as a static page — deploy by enabling GitHub Pages on this repo (`Settings → Pages → Deploy from branch → main → /root`).

## Author

Kaviya Gopal — MSc Financial Engineering & Management, KIT. Background in post-trade operations (JPMorgan CIB) and data analytics (TUI Group), applying to BASF's Controlling trainee track.
