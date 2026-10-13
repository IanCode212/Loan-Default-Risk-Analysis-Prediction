"""
Loads application_train.csv and application_test.csv into a local MySQL database.
Password is read from a .env file in the project root (git-ignored).
"""

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

DB_USER = "root"
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "credit_risk"

FILES = {
    "applications": ROOT / "data" / "application_train.csv",
    "applications_test": ROOT / "data" / "application_test.csv",
}


def main():
    engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    for table_name, csv_path in FILES.items():
        print(f"Reading {csv_path} ...")
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df):,} rows, {df.shape[1]} columns")

        print(f"Writing to MySQL table '{table_name}' ...")
        df.to_sql(table_name, engine, if_exists="replace", index=False, chunksize=5000)

    print("Done. You can now query both tables from MySQL Workbench or your notebooks.")


if __name__ == "__main__":
    main()
