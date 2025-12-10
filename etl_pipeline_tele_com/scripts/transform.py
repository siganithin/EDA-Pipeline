import os
import pandas as pd

# ---------------------------------------------
# Transform Telco Dataset
# ---------------------------------------------
def transform_telco(df: pd.DataFrame) -> pd.DataFrame:

    # 1) CLEANING ------------------------------
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    for col in ["tenure", "MonthlyCharges", "TotalCharges"]:
        df[col] = df[col].fillna(df[col].median())

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].fillna("Unknown")

    # 2) FEATURE ENGINEERING -------------------

    # tenure_group
    def tenure_group(x):
        if x <= 12: return "New"
        if x <= 36: return "Regular"
        if x <= 60: return "Loyal"
        return "Champion"

    df["tenure_group"] = df["tenure"].apply(tenure_group)

    # monthly_charge_segment
    def charge_seg(x):
        if x < 30: return "Low"
        if x <= 70: return "Medium"
        return "High"

    df["monthly_charge_segment"] = df["MonthlyCharges"].apply(charge_seg)

    # has_internet_service
    df["has_internet_service"] = df["InternetService"].map({
        "DSL": 1,
        "Fiber optic": 1,
        "No": 0
    })

    # is_multi_line_user
    df["is_multi_line_user"] = df["MultipleLines"].apply(
        lambda x: 1 if x == "Yes" else 0
    )

    # contract_type_code
    df["contract_type_code"] = df["Contract"].map({
        "Month-to-month": 0,
        "One year": 1,
        "Two year": 2
    })

    # 3) DROP UNUSED ----------------------------
    df.drop(columns=["customerID", "gender"], inplace=True, errors="ignore")

    return df


# ---------------------------------------------
# Save transformed file
# ---------------------------------------------
def transform_file(raw_path: str) -> str:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    staged = os.path.join(base_dir, "data", "staged")
    os.makedirs(staged, exist_ok=True)

    df = pd.read_csv(raw_path)
    df = transform_telco(df)

    out = os.path.join(staged, "telco_transformed.csv")
    df.to_csv(out, index=False)

    print(f"✅ Transformed & saved to: {out}")
    return out

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, "data", "raw", "telco_raw.csv")
    print(f"Reading: {raw_path}  |  Exists: {os.path.exists(raw_path)}")
    transform_file(raw_path)
