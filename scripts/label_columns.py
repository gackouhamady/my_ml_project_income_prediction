from pathlib import Path
import argparse
import pandas as pd

SCHEMA = [
    "age","class_of_worker","detailed_industry_recode","detailed_occupation_recode","education",
    "wage_per_hour","enrolled_in_edu_inst_last_wk","marital_status","major_industry_code",
    "major_occupation_code","race","hispanic_origin","sex","member_of_a_labor_union",
    "reason_for_unemployment","full_or_part_time_employment_stat","capital_gains","capital_losses",
    "dividends_from_stocks","tax_filer_status","region_of_previous_residence","state_of_previous_residence",
    "detailed_household_and_family_stat","detailed_household_summary_in_household","instance_weight",
    "migration_code_change_in_msa","migration_code_change_in_reg","migration_code_move_within_reg",
    "live_in_this_house_1_year_ago","migration_prev_res_in_sunbelt","num_persons_worked_for_employer",
    "family_members_under_18","country_of_birth_father","country_of_birth_mother","country_of_birth_self",
    "citizenship","own_business_or_self_employed","fill_inc_questionnaire_for_veterans_admin",
    "veterans_benefits","weeks_worked_in_year","year","income_raw"
]

def read_no_header(p: Path) -> pd.DataFrame:
    """
    Read a no-header CSV. Try comma-separated first, then fall back to whitespace.
    Keep all columns as object to avoid unintended type coercions at this stage.
    """
    try:
        df = pd.read_csv(p, header=None, dtype="object")
    except Exception:
        df = pd.read_csv(p, header=None, sep=r"\s+", engine="python", dtype="object")

    if df.shape[1] != len(SCHEMA):
        raise ValueError(f"Expected {len(SCHEMA)} cols, got {df.shape[1]} in {p}")
    return df

def _normalize_income_label(val) -> "pd._libs.missing.NAType | int":
    """
    Map raw income labels to binary:
      - 0 for <=50K or '- 50000' variants
      - 1 for >50K or '50000+' variants
    Preserve missing/unknown as NA.
    """
    if pd.isna(val):
        return pd.NA

    # String sanitize
    s = str(val).strip()
    s = s.replace(".", "")               # drop trailing periods
    s = " ".join(s.split())              # collapse internal whitespace

    # Canonical variants we have seen across Census/Adult datasets
    zero_set = {
        "<=50K", "<= 50K", "<=50000", "<= 50000", "<=50k", "<= 50k",
        "- 50000", "-50000", "≤50K", "≤ 50K"
    }
    one_set = {
        ">50K", "> 50K", ">50000", "> 50000", ">50k", "> 50k",
        "50000+", "50K+", "50k+"
    }

    if s in zero_set:
        return 0
    if s in one_set:
        return 1

    # Some sources encode with commas/spaces or different symbols; try light normalization
    s_norm = s.replace(",", "").replace("≤", "<=").replace("≥", ">=")

    if s_norm in zero_set:
        return 0
    if s_norm in one_set:
        return 1

    # Unknown label -> NA (do NOT coerce to 0/1)
    return pd.NA

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)

    # Read & set schema
    df = read_no_header(args.input)
    df.columns = SCHEMA

    # Trim whitespace on object columns (safe and future-proof vs applymap)
    obj_cols = df.select_dtypes(include="object").columns
    df[obj_cols] = df[obj_cols].apply(lambda s: s.str.strip())

    # Normalize income labels -> binary {0,1}, preserve missing as <NA>
    df["income_binary"] = df["income_raw"].map(_normalize_income_label).astype("Int64")

    # Write
    df.to_csv(args.output, index=False)
