from pathlib import Path
import pandas as pd

# ----- inputs / outputs -----
candidates = [
    Path("data/processed/train_labeled.csv"),
    Path("data/processed/census_income_labeled.csv"),
]
src = next((p for p in candidates if p.exists()), None)
if src is None:
    raise SystemExit("No labeled file found in data/processed/. Run label_columns.py first.")

out_dir = Path("reports/metrics"); out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "data_quality_summary.csv"

# ----- load -----
df = pd.read_csv(src)

# numeric columns in this dataset (keep if present)
num_cols = [c for c in [
    "age","wage_per_hour","capital_gains","capital_losses","dividends_from_stocks",
    "num_persons_worked_for_employer","weeks_worked_in_year","instance_weight","year"
] if c in df.columns]

# coerce numerics
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")

n = len(df)
missing = df.isna().sum()

rows = []
for col in df.columns:
    dtype = str(df[col].dtype)
    n_miss = int(missing[col])
    pct_miss = round(100 * n_miss / n, 4)

    n_out = 0; pct_out = 0.0; q1 = q3 = low = high = ""
    if col in num_cols:
        s = df[col].dropna()
        if len(s) >= 5:
            q1 = s.quantile(0.25); q3 = s.quantile(0.75)
            iqr = q3 - q1
            low = q1 - 1.5*iqr; high = q3 + 1.5*iqr
            n_out = int(((df[col] < low) | (df[col] > high)).sum())
            pct_out = round(100 * n_out / n, 4)

    rows.append({
        "column": col, "dtype": dtype,
        "n_missing": n_miss, "pct_missing": pct_miss,
        "n_outliers": n_out, "pct_outliers": pct_out,
        "q1": q1, "q3": q3, "iqr_low": low, "iqr_high": high
    })

pd.DataFrame(rows).sort_values(
    ["pct_missing","pct_outliers"], ascending=False
).to_csv(out_path, index=False)

print(f"✅ saved {out_path}")
