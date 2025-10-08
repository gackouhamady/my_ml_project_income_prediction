from pathlib import Path
import re
import pandas as pd

# ---- locate data ----
candidates = [
    Path("data/processed/train_labeled.csv"),
    Path("data/processed/census_income_labeled.csv"),
]
src = next((p for p in candidates if p.exists()), None)
if src is None:
    raise SystemExit("No labeled file found. Run scripts/label_columns.py first.")

out_metrics = Path("reports/metrics"); out_metrics.mkdir(parents=True, exist_ok=True)
out_fig = Path("reports/figures"); out_fig.mkdir(parents=True, exist_ok=True)

# ---- load ----
df = pd.read_csv(src)

# ---- robust target mapping (if needed) ----
def map_income(x):
    s = re.sub(r"[^\w<>+\-]", "", str(x)).lower()
    if "50k" in s and (">" in s or "+" in s): return 1
    if "50k" in s and ("<=" in s or "-" in s): return 0
    return None

if "income_binary" not in df.columns or df["income_binary"].isna().all():
    df["income_binary"] = df["income_raw"].map(map_income)

df = df[df["income_binary"].isin([0,1])].copy()

# ---- class balance ----
cb = df["income_binary"].value_counts(dropna=False).rename_axis("income_binary").to_frame("count")
cb["pct"] = (cb["count"] / cb["count"].sum() * 100).round(3)
cb.to_csv(out_metrics / "class_balance.csv")

# ---- categorical profiles (top 20 per feature) ----
cat_cols = [c for c in [
    "education","marital_status","class_of_worker","major_industry_code",
    "major_occupation_code","sex","race","citizenship","tax_filer_status",
    "family_members_under_18","hispanic_origin"
] if c in df.columns]

rows = []
for col in cat_cols:
    g = df.groupby(col, dropna=False)["income_binary"]
    tmp = pd.DataFrame({
        "feature": col,
        "category": g.count().index,
        "count": g.count().values,
        "pos_rate": g.mean().values,
    }).sort_values("count", ascending=False).head(20)
    rows.append(tmp)

if rows:
    cat_prof = pd.concat(rows, ignore_index=True)
    cat_prof["pos_rate"] = cat_prof["pos_rate"].round(4)
    cat_prof.to_csv(out_metrics / "cat_profiles.csv", index=False)

# ---- numeric summary ----
num_cols = [c for c in [
    "age","wage_per_hour","capital_gains","capital_losses","dividends_from_stocks",
    "num_persons_worked_for_employer","weeks_worked_in_year","instance_weight","year"
] if c in df.columns]

for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")

def q(s, p): return s.quantile(p) if s.notna().sum() else None

rows = []
for c in num_cols:
    s = df[c]
    rows.append({
        "feature": c,
        "count": int(s.notna().sum()),
        "missing": int(s.isna().sum()),
        "mean": s.mean(),
        "std": s.std(),
        "p01": q(s, 0.01),
        "p50": q(s, 0.50),
        "p99": q(s, 0.99),
    })
pd.DataFrame(rows).to_csv(out_metrics / "numeric_summary.csv", index=False)

# ---- tiny optional plots ----
try:
    import matplotlib.pyplot as plt
    ax = cb["count"].plot(kind="bar"); ax.set_title("Class balance"); ax.set_xlabel("class"); ax.set_ylabel("count")
    plt.tight_layout(); plt.savefig(out_fig / "class_balance.png"); plt.close()
    if "age" in df.columns:
        ax = df["age"].dropna().plot(kind="hist", bins=30); ax.set_title("Age distribution"); ax.set_xlabel("age")
        plt.tight_layout(); plt.savefig(out_fig / "age_hist.png"); plt.close()
except Exception:
    pass

print("✅ saved:",
      out_metrics / "class_balance.csv",
      out_metrics / "cat_profiles.csv",
      out_metrics / "numeric_summary.csv")
