from csv import DictReader
from pathlib import Path

from db import get_connection


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "employer_links.csv"


UPDATE_EMPLOYER_SQL = """
    UPDATE target_employers
    SET
        company_url = NULLIF(%s, ''),
        careers_url = NULLIF(%s, ''),
        linkedin_url = NULLIF(%s, ''),
        links_updated_at = NOW()
    WHERE LOWER(TRIM(company_name)) = LOWER(TRIM(%s))
    RETURNING employer_id, company_name;
"""


def load_rows(csv_path: Path) -> list[dict[str, str]]:
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Employer links file was not found:\n{csv_path}"
        )

    try:
        with csv_path.open(
            mode="r",
            encoding="utf-8-sig",
            newline="",
        ) as csv_file:
            return list(DictReader(csv_file))

    except UnicodeDecodeError:
        with csv_path.open(
            mode="r",
            encoding="cp1252",
            newline="",
        ) as csv_file:
            return list(DictReader(csv_file))


def validate_columns(rows: list[dict[str, str]]) -> None:
    required_columns = {
        "company_name",
        "company_url",
        "careers_url",
        "linkedin_url",
    }

    if not rows:
        raise ValueError("The employer links CSV is empty.")

    available_columns = set(rows[0].keys())
    missing_columns = required_columns - available_columns

    if missing_columns:
        missing_text = ", ".join(sorted(missing_columns))
        raise ValueError(
            f"The CSV is missing required columns: {missing_text}"
        )


def clean_value(value: str | None) -> str:
    if value is None:
        return ""

    return value.strip()


def enrich_employers(rows: list[dict[str, str]]) -> tuple[int, list[str]]:
    updated_count = 0
    unmatched_companies = []

    with get_connection() as connection:
        with connection.cursor() as cursor:
            for row in rows:
                company_name = clean_value(row.get("company_name"))

                if not company_name:
                    continue

                company_url = clean_value(row.get("company_url"))
                careers_url = clean_value(row.get("careers_url"))
                linkedin_url = clean_value(row.get("linkedin_url"))

                cursor.execute(
                    UPDATE_EMPLOYER_SQL,
                    (
                        company_url,
                        careers_url,
                        linkedin_url,
                        company_name,
                    ),
                )

                result = cursor.fetchone()

                if result is None:
                    unmatched_companies.append(company_name)
                    continue

                employer_id, matched_company_name = result

                print(
                    f"Updated {employer_id}: "
                    f"{matched_company_name}"
                )

                updated_count += 1

        connection.commit()

    return updated_count, unmatched_companies


def main() -> None:
    try:
        rows = load_rows(CSV_PATH)
        validate_columns(rows)

        updated_count, unmatched_companies = enrich_employers(rows)

        print()
        print(f"Updated employers: {updated_count}")
        print(f"Unmatched employers: {len(unmatched_companies)}")

        if unmatched_companies:
            print("\nNames not found in target_employers:")

            for company_name in unmatched_companies:
                print(f"  - {company_name}")

    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")

    except Exception as error:
        print(f"Unexpected error: {error}")
        raise


if __name__ == "__main__":
    main()