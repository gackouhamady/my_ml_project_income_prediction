from pathlib import Path
import argparse, pandas as pd

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

TARGET = {"- 50000":0,"50000+":1,"<=50K":0,">50K":1,"<=50K.":0,">50K.":1}

def read_no_header(p: Path) -> pd.DataFrame:
    # Try comma-separated first, then whitespace
    try:
        df = pd.read_csv(p, header=None, dtype="object")
    except Exception:
        df = pd.read_csv(p, header=None, sep=r"\s+", engine="python", dtype="object")
    if df.shape[1] != len(SCHEMA):
        raise ValueError(f"Expected {len(SCHEMA)} cols, got {df.shape[1]} in {p}")
    return df

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    df = read_no_header(args.input)
    df.columns = SCHEMA
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df["income_binary"] = df["income_raw"].replace({"<=50K.":"<=50K",">50K.":">50K"}).map(TARGET)
    df.to_csv(args.output, index=False)
