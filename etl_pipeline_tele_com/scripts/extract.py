import os, pandas as pd

def extract_telco(source_csv_path: str) -> str:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)

    df = pd.read_csv(source_csv_path)
    raw_path = os.path.join(raw_dir, "telco_raw.csv")
    df.to_csv(raw_path, index=False)
    print(f"✅ Extracted Telco data to: {raw_path}")
    return raw_path

if __name__ == "__main__":
    extract_telco(r"C:\aids\week8_etl_pipeline\etl_pipeline_tele_com\WA_Fn-UseC_-Telco-Customer-Churn.csv")
