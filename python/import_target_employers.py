from pathlib import Path
import os

import pandas as pd
import psycopg
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

CSV_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "target_companies.csv"
)


def clean_value(value):
    """Convert pandas NaN values to Python None for PostgreSQL."""
    if pd.isna(value):
        return None

    value = str(value).strip()
    return value or None


def main():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is missing from the .env file.")

    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV not found: {CSV_PATH}")

    dataframe = pd.read_csv(CSV_PATH, encoding="cp1252")

    required_columns = {
        "Canonical Company",
        "Register Organisation Name",
        "Town/City",
        "County",
        "Type & Rating",
        "Route",
        "Sector",
        "Priority",
        "Target Roles",
        "Search Frequency",
        "Notes",
    }

    missing_columns = required_columns - set(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"CSV is missing required columns: {sorted(missing_columns)}"
        )

    sql = """
        INSERT INTO target_employers (
            company_name,
            register_name,
            town_city,
            county,
            sector,
            priority,
            licence_type,
            visa_route,
            target_roles,
            search_frequency,
            notes
        )
        VALUES (
            %(company_name)s,
            %(register_name)s,
            %(town_city)s,
            %(county)s,
            %(sector)s,
            %(priority)s,
            %(licence_type)s,
            %(visa_route)s,
            %(target_roles)s,
            %(search_frequency)s,
            %(notes)s
        )
        ON CONFLICT (company_name)
        DO UPDATE SET
            register_name = EXCLUDED.register_name,
            town_city = EXCLUDED.town_city,
            county = EXCLUDED.county,
            sector = EXCLUDED.sector,
            priority = EXCLUDED.priority,
            licence_type = EXCLUDED.licence_type,
            visa_route = EXCLUDED.visa_route,
            target_roles = EXCLUDED.target_roles,
            search_frequency = EXCLUDED.search_frequency,
            notes = EXCLUDED.notes;
    """

    records = []

    for _, row in dataframe.iterrows():
        records.append(
            {
                "company_name": clean_value(row["Canonical Company"]),
                "register_name": clean_value(
                    row["Register Organisation Name"]
                ),
                "town_city": clean_value(row["Town/City"]),
                "county": clean_value(row["County"]),
                "sector": clean_value(row["Sector"]),
                "priority": clean_value(row["Priority"]),
                "licence_type": clean_value(row["Type & Rating"]),
                "visa_route": clean_value(row["Route"]),
                "target_roles": clean_value(row["Target Roles"]),
                "search_frequency": clean_value(
                    row["Search Frequency"]
                ),
                "notes": clean_value(row["Notes"]),
            }
        )

    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.executemany(sql, records)

    print(f"Imported or updated {len(records)} target employers.")


if __name__ == "__main__":
    main()