import pandas as pd
import sqlite3

EXCEL_PATH = "data/HR_Agent_Sample_Data.xlsx"
DB_PATH = "db/hr_agent.db"

def ingest_excel():
    conn = sqlite3.connect(DB_PATH)
    excel_file = pd.ExcelFile(EXCEL_PATH)
    print("\nSheets Found:")
    print(excel_file.sheet_names)

    for sheet in excel_file.sheet_names:
        print(f"\nProcessing: {sheet}")
        df = pd.read_excel(
            EXCEL_PATH,
            sheet_name=sheet,
            header=1
        )
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )
        table_name = (
            sheet.lower()
            .replace(" ", "_")
        )
        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )
        print(
            f"Inserted {len(df)} rows "
            f"into table '{table_name}'"
        )
    conn.close()
    print("\nSQLite ingestion complete!")

if __name__ == "__main__":
    ingest_excel()