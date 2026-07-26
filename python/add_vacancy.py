from datetime import datetime
from urllib.parse import urlparse

from db import get_connection


def get_employers():
    sql = """
        SELECT
            employer_id,
            company_name
        FROM target_employers
        ORDER BY company_name;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()


def display_employers(employers):
    print("\nTarget employers\n")
    print(f"{'ID':<6}{'Company'}")
    print("-" * 60)

    for employer_id, company_name in employers:
        print(f"{employer_id:<6}{company_name}")


def prompt_required(label):
    while True:
        value = input(f"{label}: ").strip()

        if value:
            return value

        print(f"{label} is required.")


def prompt_optional(label):
    value = input(f"{label} (optional): ").strip()
    return value or None


def prompt_date(label):
    while True:
        value = input(
            f"{label} in YYYY-MM-DD format (optional): "
        ).strip()

        if not value:
            return None

        try:
            return datetime.strptime(value, "%Y-%m-%d").date()

        except ValueError:
            print("Please use YYYY-MM-DD, for example 2026-08-15.")


def prompt_employer_id(valid_ids):
    while True:
        value = input(
            "\nEnter the employer ID: "
        ).strip()

        try:
            employer_id = int(value)

        except ValueError:
            print("Please enter a numeric employer ID.")
            continue

        if employer_id not in valid_ids:
            print("That employer ID is not in the list.")
            continue

        return employer_id


def is_valid_url(value):
    parsed = urlparse(value)

    return (
        parsed.scheme in {"http", "https"}
        and bool(parsed.netloc)
    )


def prompt_url():
    while True:
        value = prompt_required("Vacancy URL")

        if is_valid_url(value):
            return value

        print(
            "Please enter a complete URL beginning with "
            "http:// or https://"
        )


def vacancy_exists(vacancy_url):
    sql = """
        SELECT
            vacancy_id,
            title
        FROM vacancies
        WHERE vacancy_url = %s;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, (vacancy_url,))
            return cursor.fetchone()


def add_vacancy(
    employer_id,
    title,
    location,
    salary,
    contract_type,
    closing_date,
    vacancy_url,
    notes,
):
    sql = """
        INSERT INTO vacancies (
            employer_id,
            title,
            location,
            salary,
            contract_type,
            closing_date,
            vacancy_url,
            notes
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        RETURNING vacancy_id;
    """

    values = (
        employer_id,
        title,
        location,
        salary,
        contract_type,
        closing_date,
        vacancy_url,
        notes,
    )

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, values)
            vacancy_id = cursor.fetchone()[0]

        connection.commit()

    return vacancy_id


def main():
    employers = get_employers()

    if not employers:
        print("No target employers were found.")
        return

    display_employers(employers)

    valid_ids = {
        employer_id
        for employer_id, _ in employers
    }

    employer_id = prompt_employer_id(valid_ids)
    title = prompt_required("Job title")
    location = prompt_optional("Location")
    salary = prompt_optional("Salary")
    contract_type = prompt_optional("Contract type")
    closing_date = prompt_date("Closing date")
    vacancy_url = prompt_url()
    notes = prompt_optional("Notes")

    duplicate = vacancy_exists(vacancy_url)

    if duplicate:
        vacancy_id, existing_title = duplicate

        print(
            "\nThis vacancy is already stored:"
            f"\nID: {vacancy_id}"
            f"\nTitle: {existing_title}"
        )
        return

    vacancy_id = add_vacancy(
        employer_id=employer_id,
        title=title,
        location=location,
        salary=salary,
        contract_type=contract_type,
        closing_date=closing_date,
        vacancy_url=vacancy_url,
        notes=notes,
    )

    print(
        f"\nVacancy saved successfully with ID {vacancy_id}."
    )


if __name__ == "__main__":
    main()