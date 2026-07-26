import webbrowser
from datetime import date

from db import get_connection


VALID_STATUSES = {
    "Open",
    "Considering",
    "Applied",
    "Closed",
    "Rejected",
    "Ignored",
}


def get_vacancies(status="Open"):
    sql = """
        SELECT
            v.vacancy_id,
            te.company_name,
            v.title,
            v.location,
            v.salary,
            v.closing_date,
            v.status,
            v.vacancy_url
        FROM vacancies AS v
        JOIN target_employers AS te
            ON te.employer_id = v.employer_id
        WHERE v.status = %s
        ORDER BY
            v.closing_date NULLS LAST,
            te.company_name,
            v.title;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, (status,))
            return cursor.fetchall()


def display_vacancies(vacancies):
    if not vacancies:
        print("\nNo matching vacancies were found.")
        return

    print("\nVacancies\n")

    for vacancy in vacancies:
        (
            vacancy_id,
            company_name,
            title,
            location,
            salary,
            closing_date,
            status,
            vacancy_url,
        ) = vacancy

        closing_text = (
            closing_date.strftime("%d %b %Y")
            if closing_date
            else "Not stated"
        )

        if closing_date and closing_date < date.today():
            closing_text += " — passed"

        print(f"[{vacancy_id}] {title}")
        print(f"    Employer: {company_name}")
        print(f"    Location: {location or 'Not stated'}")
        print(f"    Salary: {salary or 'Not stated'}")
        print(f"    Closing: {closing_text}")
        print(f"    Status: {status}")
        print()


def get_vacancy(vacancy_id):
    sql = """
        SELECT
            te.company_name,
            v.title,
            v.vacancy_url,
            v.status
        FROM vacancies AS v
        JOIN target_employers AS te
            ON te.employer_id = v.employer_id
        WHERE v.vacancy_id = %s;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, (vacancy_id,))
            return cursor.fetchone()


def update_status(vacancy_id, status):
    sql = """
        UPDATE vacancies
        SET status = %s
        WHERE vacancy_id = %s
        RETURNING vacancy_id;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    status,
                    vacancy_id,
                ),
            )
            result = cursor.fetchone()

        connection.commit()

    return result is not None


def choose_status():
    print("\nAvailable statuses:")

    statuses = sorted(VALID_STATUSES)

    for index, status in enumerate(statuses, start=1):
        print(f"{index}. {status}")

    value = input(
        "\nSelect a status number: "
    ).strip()

    try:
        index = int(value) - 1
        return statuses[index]

    except (ValueError, IndexError):
        print("Invalid status selection.")
        return None


def main():
    status_filter = input(
        "Status to list [Open]: "
    ).strip().title()

    if not status_filter:
        status_filter = "Open"

    if status_filter not in VALID_STATUSES:
        print(
            "Unknown status. Valid statuses are: "
            + ", ".join(sorted(VALID_STATUSES))
        )
        return

    vacancies = get_vacancies(status_filter)
    display_vacancies(vacancies)

    if not vacancies:
        return

    choice = input(
        "Enter a vacancy ID to manage, "
        "or press Enter to exit: "
    ).strip()

    if not choice:
        return

    try:
        vacancy_id = int(choice)

    except ValueError:
        print("Please enter a numeric vacancy ID.")
        return

    vacancy = get_vacancy(vacancy_id)

    if vacancy is None:
        print("Vacancy not found.")
        return

    company_name, title, vacancy_url, current_status = vacancy

    print(f"\n{title}")
    print(f"Employer: {company_name}")
    print(f"Current status: {current_status}")

    print(
        "\n1. Open vacancy page"
        "\n2. Change status"
        "\n3. Exit"
    )

    action = input("\nChoose an action: ").strip()

    if action == "1":
        if vacancy_url:
            print(f"Opening {vacancy_url}")
            webbrowser.open_new_tab(vacancy_url)
        else:
            print("No URL is stored for this vacancy.")

    elif action == "2":
        new_status = choose_status()

        if new_status is None:
            return

        if update_status(vacancy_id, new_status):
            print(
                f"Vacancy status changed to {new_status}."
            )
        else:
            print("The vacancy could not be updated.")

    elif action == "3":
        return

    else:
        print("Invalid action.")


if __name__ == "__main__":
    main()