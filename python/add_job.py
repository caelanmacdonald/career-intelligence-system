"""Add a job vacancy to the Career Intelligence Dashboard database."""

from datetime import date

from db import get_connection


def prompt_optional(label: str) -> str | None:
    """Return user input, or None when left blank."""
    value = input(f"{label}: ").strip()
    return value or None


def prompt_optional_integer(label: str) -> int | None:
    """Return an integer, or None when left blank."""
    value = input(f"{label}: ").strip()

    if not value:
        return None

    try:
        return int(value)
    except ValueError:
        raise ValueError(f"{label} must be a whole number.")


def prompt_optional_date(label: str) -> date | None:
    """Return a date in YYYY-MM-DD format, or None when left blank."""
    value = input(f"{label} (YYYY-MM-DD): ").strip()

    if not value:
        return None

    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"{label} must use YYYY-MM-DD format.")


def display_companies() -> None:
    """Print available companies and their IDs."""

    query = """
        SELECT
            company_id,
            company_name
        FROM companies
        ORDER BY company_name;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            companies = cursor.fetchall()

    if not companies:
        print("No companies found. Add a company before adding a job.")
        return

    print("\nAvailable companies:\n")

    for company_id, company_name in companies:
        print(f"{company_id}: {company_name}")


def add_job() -> None:
    """Prompt for job details and insert the vacancy into PostgreSQL."""

    print("\nAdd a new job vacancy\n")

    display_companies()

    try:
        company_id = int(input("\nCompany ID: ").strip())
    except ValueError:
        print("Company ID must be a whole number.")
        return

    job_title = input("Job title: ").strip()

    if not job_title:
        print("Job title is required.")
        return

    try:
        location = prompt_optional("Location")
        salary_min = prompt_optional_integer("Minimum salary")
        salary_max = prompt_optional_integer("Maximum salary")
        employment_type = prompt_optional("Employment type")
        sponsorship_status = prompt_optional("Sponsorship status")
        closing_date = prompt_optional_date("Closing date")
        job_url = prompt_optional("Job URL")
        job_status = prompt_optional("Job status") or "Open"
        notes = prompt_optional("Notes")
    except ValueError as error:
        print(error)
        return

    if (
        salary_min is not None
        and salary_max is not None
        and salary_min > salary_max
    ):
        print("Minimum salary cannot be greater than maximum salary.")
        return

    query = """
        INSERT INTO jobs (
            company_id,
            job_title,
            location,
            salary_min,
            salary_max,
            employment_type,
            sponsorship_status,
            closing_date,
            job_url,
            job_status,
            notes
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING job_id;
    """

    values = (
        company_id,
        job_title,
        location,
        salary_min,
        salary_max,
        employment_type,
        sponsorship_status,
        closing_date,
        job_url,
        job_status,
        notes,
    )

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, values)
                job_id = cursor.fetchone()[0]

        print(f"\nJob added successfully with ID {job_id}.")

    except Exception as error:
        print(f"\nCould not add job: {error}")


if __name__ == "__main__":
    add_job()