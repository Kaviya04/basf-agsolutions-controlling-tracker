import csv, json, re

def parse_num(s):
    s = s.strip()
    if s == '':
        return None
    neg = s.startswith('-')
    s = s.replace('-','').replace(',','')
    try:
        v = float(s)
    except:
        return None
    return -v if neg else v

def load(path):
    with open(path, encoding='utf-8-sig') as f:
        rows = list(csv.reader(f))
    header_idx = None
    for i,r in enumerate(rows):
        if r and r[0]=='' and len(r)>1 and re.match(r'\d{2}/\d{2}/\d{4}', r[1] or ''):
            header_idx = i
            break
    years = [c[-4:] for c in rows[header_idx][1:] if c]
    data = {}
    for r in rows[header_idx+1:]:
        if not r or not r[0]:
            continue
        label = r[0].strip()
        if label.lower() in ('currency','source'):
            continue
        vals = [parse_num(x) for x in r[1:1+len(years)]]
        data[label] = dict(zip(years, vals))
    return years, data

years, income = load('income_basf_se.csv')
_, balance = load('balance_basf_se.csv')

M = 1_000_000  # convert to EUR million

def g(d, key, y):
    v = d.get(key, {}).get(y)
    return None if v is None else v / M

series = []
for y in years:
    rev = g(income, '1. Revenue', y)
    cogs = g(income, '2. Cost of Revenue', y)
    gp = g(income, '3. Gross Profit', y)
    opex = g(income, '4. Operating Expenses', y)
    sga = g(income, 'a) Selling General and Administrative Expenses', y)
    rnd = g(income, 'b) Research and Development Expenses', y)
    ebit = g(income, '5. Operating Income', y)
    other = g(income, '6. Total other income expenses net', y)
    da = g(income, '7. Depreciation and Amortization', y)
    ebitda = g(income, '8. EBITDA', y)
    ebt = g(income, '9. Income before Tax', y)
    tax = g(income, '10. Income Tax Expense', y)
    ni = g(income, '11. Net Income', y)

    total_assets = g(balance, 'A. Total Assets', y)
    total_equity = g(balance, 'II. Total Equity', y)
    total_liab = g(balance, 'I. Total Liabilities', y)
    cash = g(balance, 'a) Cash and Cash Equivalents', y)
    st_debt = g(balance, 'ac) Short Term Debt', y)
    lt_debt = g(balance, 'ba) Long Term Debt', y)
    inventory = g(balance, 'c) Inventory', y)
    receivables = g(balance, 'd) Net Receivables', y)
    payables = g(balance, 'ab) Account Payables', y)
    curr_assets = g(balance, 'I. Total Current Assets', y)
    curr_liab = g(balance, 'a) Total Current Liabilities', y)

    net_debt = (st_debt or 0) + (lt_debt or 0) - (cash or 0)
    equity_ratio = total_equity / total_assets * 100 if total_assets else None
    ebit_margin = ebit / rev * 100 if rev else None
    ebitda_margin = ebitda / rev * 100 if rev else None
    net_margin = ni / rev * 100 if rev else None
    current_ratio = curr_assets / curr_liab if curr_liab else None
    net_debt_ebitda = net_debt / ebitda if ebitda else None
    wc = (inventory or 0) + (receivables or 0) - (payables or 0)
    wc_pct_rev = wc / rev * 100 if rev else None
    roe = ni / total_equity * 100 if total_equity else None

    series.append(dict(
        year=int(y), revenue=rev, cogs=cogs, gross_profit=gp, sga=sga, rnd=rnd,
        opex=opex, ebit=ebit, other_income=other, da=da, ebitda=ebitda,
        ebt=ebt, tax=tax, net_income=ni,
        total_assets=total_assets, total_equity=total_equity, total_liabilities=total_liab,
        net_debt=round(net_debt,1), equity_ratio=equity_ratio, ebit_margin=ebit_margin,
        ebitda_margin=ebitda_margin, net_margin=net_margin, current_ratio=current_ratio,
        net_debt_ebitda=net_debt_ebitda, working_capital=round(wc,1), wc_pct_rev=wc_pct_rev,
        roe=roe
    ))

# round all floats to 1 decimal
def r1(x):
    return None if x is None else round(x,1)

for row in series:
    for k,v in row.items():
        if isinstance(v,float):
            row[k]=r1(v)

with open('data.json','w') as f:
    json.dump(series, f, indent=2)

print(json.dumps(series[-5:], indent=2))
