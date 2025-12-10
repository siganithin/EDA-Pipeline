import os
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client

# ---------------------------------------------
# Supabase Client
# ---------------------------------------------
def get_supabase_client():
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("❌ Missing SUPABASE_URL or SUPABASE_KEY in .env")

    return create_client(url, key)

TABLE = "telco_churn"


# ---------------------------------------------
# LOAD TO SUPABASE
# ---------------------------------------------
def load_to_supabase(csv_path: str):
    sb = get_supabase_client()

    if not os.path.exists(csv_path):
        print(f"❌ Not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    df = df.where(pd.notnull(df), None)  # NaN → None

    rows = df.to_dict("records")
    print(f"📦 Uploading {len(rows)} rows → {TABLE}")

    batch = 800
    for i in range(0, len(rows), batch):
        part = rows[i:i + batch]

        try:
            sb.table(TABLE).upsert(part).execute()
            print(f"✅ Rows {i+1} → {min(i+batch, len(rows))}")
        except Exception as e:
            print(f"⚠️ Error batch {i//batch+1}: {e}")

    print("🎉 Completed upload!")


if __name__ == "__main__":
    import os

    # Resolve path relative to project root (one level up from /scripts)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "staged", "telco_transformed.csv")

    print(f"Reading: {csv_path}  |  Exists: {os.path.exists(csv_path)}")
    load_to_supabase(csv_path)
