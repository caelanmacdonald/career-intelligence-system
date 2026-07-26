import webbrowser
from datetime import datetime, timezone

from db import get_connection


def get_employers(priority: str = "A"):
    sql = """
        SELECT
            employer_id,
            company_name,
            sector,
            last_checked,
            careers_url
        FROM target_employers
        WHERE priority = %s
        ORDER BY
            last_checked NULLS FIRST,
            company_name;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, (priority,))
            return cursor.fetchall()


def display_employers(employers) -> None:
    print("\nPriority A employers\n")

    print(
        f"{'ID':<5}"
        f"{'Company':<36}"
        f"{'Sector':<30}"
        f"{'Portal':<10}"
        f"{'Last checked'}"
    )

    print("-" * 105)

    for employer in employers:
        (
            employer_id,
            company_name,
            sector,
            last_checked,
            careers_url,
        ) = employer

        checked_text = (
            last_checked.astimezone().strftime("%d %b %Y %H:%M")
            if last_checked
            else "Never"
        )

        portal_text = "Linked" if careers_url else "Missing"

        print(
            f"{employer_id:<5}"
            f"{company_name:<36}"
            f"{(sector or 'Unknown'):<30}"
            f"{portal_text:<10}"
            f"{checked_text}"
        )


def get_employer(employer_id: int):
    sql = """
        SELECT
            company_name,
            careers_url
        FROM target_employers
        WHERE employer_id = %s;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, (employer_id,))
            return cursor.fetchone()


def open_careers_portal(
    company_name: str,
    careers_url: str | None,
) -> bool:
    if not careers_url:
        print(
            f"\nNo careers portal is stored for {company_name}."
        )
        return False

    print(f"\nOpening {company_name} careers portal...")
    print(careers_url)

    opened = webbrowser.open_new_tab(careers_url)

    if not opened:
        print(
            "\nThe browser did not report a successful launch."
        )
        print("Copy the URL above into your browser manually.")
        return False

    return True


def mark_checked(employer_id: int) -> str | None:
    sql = """
        UPDATE target_employers
        SET last_checked = %s
        WHERE employer_id = %s
        RETURNING company_name;
    """

    checked_at = datetime.now(timezone.utc)

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    checked_at,
                    employer_id,
                ),
            )

            result = cursor.fetchone()

        connection.commit()

    if result is None:
        return None

    return result[0]


def main() -> None:
    employers = get_employers()

    if not employers:
        print("No Priority A employers were found.")
        return

    display_employers(employers)

    choice = input(
        "\nEnter an employer ID to open its careers portal, "
        "or press Enter to exit: "
    ).strip()

    if not choice:
        return

    try:
        employer_id = int(choice)

    except ValueError:
        print("Please enter a numeric employer ID.")
        return

    employer = get_employer(employer_id)

    if employer is None:
        print("Employer not found.")
        return

    company_name, careers_url = employer

    if not open_careers_portal(
        company_name,
        careers_url,
    ):
        return

    result = input(
        "\nReview the vacancies in your browser.\n"
        "Press Enter when finished to mark the employer as checked.\n"
        "Type N to leave it unchanged: "
    ).strip().lower()

    if result == "n":
        print(f"{company_name} was not marked as checked.")
        return

    updated_company = mark_checked(employer_id)

    if updated_company is None:
        print("The employer could not be updated.")
        return

    print(f"{updated_company} marked as checked.")


if __name__ == "__main__":
    main()