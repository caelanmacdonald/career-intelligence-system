"""Add a company to the Career Intelligence Dashboard database."""

from db import get_connection


def prompt_optional(label: str) -> str | None:
    """Return user input, or None when left blank."""
    value = input(f"{label}: ").strip()
    return value or None


def add_company() -> None:
    """Prompt for company details and insert the company into PostgreSQL."""

    print("\nAdd a new company\n")

    company_name = input("Company name: ").strip()

    if not company_name:
        print("Company name is required.")
        return

    sector = prompt_optional("Sector")
    sponsor_status = prompt_optional(
        "Sponsor status (Licensed / Not licensed / Unknown)"
    )
    careers_url = prompt_optional("Careers URL")
    priority = prompt_optional("Priority (A / B / C)")
    headquarters = prompt_optional("Headquarters")
    notes = prompt_optional("Notes")

    if priority:
        priority = priority.upper()

        if priority not in {"A", "B", "C"}:
            print("Priority must be A, B or C.")
            return

    query = """
        INSERT INTO companies (
            company_name,
            sector,
            sponsor_status,
            careers_url,
            priority,
            headquarters,
            notes
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING company_id;
    """

    values = (
        company_name,
        sector,
        sponsor_status,
        careers_url,
        priority,
        headquarters,
        notes,
    )

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, values)
                company_id = cursor.fetchone()[0]

        print(f"\nCompany added successfully with ID {company_id}.")

    except Exception as error:
        print(f"\nCould not add company: {error}")


if __name__ == "__main__":
    add_company()