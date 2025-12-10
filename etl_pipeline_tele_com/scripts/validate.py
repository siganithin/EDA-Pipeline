# validate.py
import os
import sys
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client

# ---- Expectations ----
REQUIRED_NUM_COLS = ["tenure", "MonthlyCharges", "TotalCharges"]
REQUIRED_TENURE_GROUPS = {"New", "Regular", "Loyal", "Champion"}
REQUIRED_CHARGE_SEGMENTS = {"Low", "Medium", "High"}
VALID_CONTRACT_CODES = {0, 1, 2}
SUPABASE_TABLE = "telco_churn"  # change via .env if you want

# ---- Path helpers ----
def project_root() -> str:
    # one level above scripts/
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_paths():
    root = project_root()
    raw_path   = os.path.join(root, "data", "raw",    "telco_raw.csv")
    clean_path = os.path.join(root, "data", "staged", "telco_transformed.csv")
    return raw_path, clean_path

# ---- Supabase helpers ----
def get_supabase_client():
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY in .env")
    return create_client(url, key)

def supabase_count(table: str):
    sb = get_supabase_client()
    resp = sb.table(table).select("*", count="exact", head=True).execute()
    return getattr(resp, "count", None)

# ---- Validation ----
def validate():
    raw_path, clean_path = get_paths()

    print("\n====== VALIDATION STARTED ======")
    print("RAW FILE   :", raw_path)
    print("CLEAN FILE :", clean_path)
    print("--------------------------------\n")

    if not os.path.exists(raw_path):
        print(f"❌ Raw file not found: {raw_path}")
        sys.exit(1)
    if not os.path.exists(clean_path):
        print(f"❌ Cleaned file not found: {clean_path}")
        sys.exit(1)

    df_raw   = pd.read_csv(raw_path)
    df_clean = pd.read_csv(clean_path)

    results = {}

    # 1) No missing values in required numeric columns
    missing_details = {c: int(df_clean[c].isna().sum()) for c in REQUIRED_NUM_COLS}
    no_missing_numeric = all(v == 0 for v in missing_details.values())
    results["no_missing_numeric"] = no_missing_numeric
    results["missing_details"] = missing_details

    # 2) Row count should match raw (we only report duplicates)
    row_count_ok = (len(df_clean) == len(df_raw))
    dup_count = int(df_clean.duplicated().sum())
    results["row_count_ok"] = row_count_ok
    results["dup_count"] = dup_count
    results["row_counts"] = {"raw": len(df_raw), "clean": len(df_clean)}

    # 3) Supabase row count equals clean
    try:
        sb_rows = supabase_count(os.getenv("SUPABASE_TABLE", SUPABASE_TABLE))
        sb_match = (sb_rows == len(df_clean))
    except Exception as e:
        sb_rows = None
        sb_match = False
        results["supabase_error"] = str(e)
    results["sb_match"] = sb_match
    results["sb_vs_clean"] = {"supabase": sb_rows, "clean": len(df_clean)}

    # 4) Tenure groups present
    tenure_found = set(df_clean["tenure_group"].unique()) if "tenure_group" in df_clean.columns else set()
    tenure_ok = REQUIRED_TENURE_GROUPS.issubset(tenure_found)
    results["tenure_ok"] = tenure_ok
    results["tenure_found"] = sorted(tenure_found)

    # 5) Charge segments present
    charge_found = set(df_clean["monthly_charge_segment"].unique()) if "monthly_charge_segment" in df_clean.columns else set()
    charge_ok = REQUIRED_CHARGE_SEGMENTS.issubset(charge_found)
    results["charge_ok"] = charge_ok
    results["charge_found"] = sorted(charge_found)

    # 6) Contract codes valid subset of {0,1,2}
    if "contract_type_code" in df_clean.columns:
        codes_series = pd.to_numeric(df_clean["contract_type_code"], errors="coerce").dropna().astype(int)
        codes_found = set(codes_series.unique())
    else:
        codes_found = set()
    codes_ok = codes_found.issubset(VALID_CONTRACT_CODES) and len(codes_found) > 0
    results["codes_ok"] = codes_ok
    results["codes_found"] = sorted(codes_found)

    # ---- Summary ----
    def tick(v): return "✅" if v else "❌"

    print("===== SUMMARY =====")
    print(f"{tick(no_missing_numeric)} No missing numerics | {missing_details}")
    print(f"{tick(row_count_ok)} Row count matches raw | {results['row_counts']}  (duplicates in clean: {dup_count})")
    if sb_rows is None:
        print(f"❌ Supabase check failed | error: {results.get('supabase_error')}")
    else:
        print(f"{tick(sb_match)} Supabase rows match clean | {results['sb_vs_clean']}")
    print(f"{tick(tenure_ok)} Tenure groups OK | found={results['tenure_found']}")
    print(f"{tick(charge_ok)} Charge segments OK | found={results['charge_found']}")
    print(f"{tick(codes_ok)} Contract codes OK | found={results['codes_found']}")
    print("====================")

    # Final pass/fail (no unique-row requirement)
    if all([no_missing_numeric, row_count_ok, sb_match, tenure_ok, charge_ok, codes_ok]):
        print("🎉 VALIDATION PASSED — ALL CHECKS SUCCESSFUL!")
        sys.exit(0)
    else:
        print("⚠️ VALIDATION FAILED — SEE ABOVE")
        sys.exit(2)

if __name__ == "__main__":
    validate()
