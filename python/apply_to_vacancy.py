from datetime import date

from db import get_connection


def get_open_vacancies():
    sql = """
        SELECT
            v.vacancy_id,
            te.company_name,
            v.title,
            v.location,
            v.closing_date
        FROM vacancies AS v
        JOIN target_employers AS te
            ON te.employer_id = v.employer_id
        WHERE v.status IN ('Open', 'Considering')
        ORDER BY
            v.closing_date NULLS LAST,
            te.company_name,
            v.title;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()


def display_vacancies(vacancies):
    if not vacancies:
        print("\nNo open vacancies were found.")
        return

    print("\nOpen vacancies\n")

    for vacancy in vacancies:
        (
            vacancy_id,
            company_name,
            title,
            location,
            closing_date,
        ) = vacancy

        closing_text = (
            closing_date.strftime("%d %b %Y")
            if closing_date
            else "Not stated"
        )

        print(f"[{vacancy_id}] {title}")
        print(f"    Employer: {company_name}")
        print(f"    Location: {location or 'Not stated'}")
        print(f"    Closing date: {closing_text}")
        print()


def choose_vacancy(valid_ids):
    while True:
        choice = input(
            "Enter a vacancy ID to apply to, "
            "or press Enter to exit: "
        ).strip()

        if not choice:
            return None

        try:
            vacancy_id = int(choice)
        except ValueError:
            print("Please enter a numeric vacancy ID.")
            continue

        if vacancy_id not in valid_ids:
            print("That vacancy ID is not in the displayed list.")
            continue

        return vacancy_id


def get_vacancy(cursor, vacancy_id):
    sql = """
        SELECT
            v.vacancy_id,
            v.employer_id,
            te.company_name,
            v.title,
            v.status
        FROM vacancies AS v
        JOIN target_employers AS te
            ON te.employer_id = v.employer_id
        WHERE v.vacancy_id = %s
        FOR UPDATE;
    """

    cursor.execute(sql, (vacancy_id,))
    return cursor.fetchone()


def application_exists(cursor, vacancy_id):
    sql = """
        SELECT application_id
        FROM applications
        WHERE vacancy_id = %s;
    """

    cursor.execute(sql, (vacancy_id,))
    return cursor.fetchone()


def create_application(cursor, vacancy_id):
    sql = """
        INSERT INTO applications (
            vacancy_id,
            date_applied,
            status
        )
        VALUES (%s, %s, %s)
        RETURNING application_id;
    """

    cursor.execute(
        sql,
        (
            vacancy_id,
            date.today(),
            "Applied",
        ),
    )

    return cursor.fetchone()[0]


def create_application_event(cursor, application_id):
    sql = """
        INSERT INTO application_events (
            application_id,
            event_type,
            event_date,
            notes
        )
        VALUES (%s, %s, %s, %s);
    """

    cursor.execute(
        sql,
        (
            application_id,
            "Applied",
            date.today(),
            "Application submitted.",
        ),
    )


def update_vacancy_status(cursor, vacancy_id):
    sql = """
        UPDATE vacancies
        SET status = 'Applied'
        WHERE vacancy_id = %s;
    """

    cursor.execute(sql, (vacancy_id,))


def apply_to_vacancy(vacancy_id):
    with get_connection() as connection:
        try:
            with connection.cursor() as cursor:
                vacancy = get_vacancy(cursor, vacancy_id)

                if vacancy is None:
                    raise ValueError("Vacancy not found.")

                (
                    vacancy_id,
                    employer_id,
                    company_name,
                    title,
                    vacancy_status,
                ) = vacancy

                if vacancy_status == "Applied":
                    raise ValueError(
                        "This vacancy is already marked as applied."
                    )

                existing_application = application_exists(
                    cursor,
                    vacancy_id,
                )

                if existing_application:
                    raise ValueError(
                        "An application already exists for this vacancy."
                    )

                application_id = create_application(
                    cursor,
                    vacancy_id,
                )

                create_application_event(
                    cursor,
                    application_id,
                )

                update_vacancy_status(
                    cursor,
                    vacancy_id,
                )

            connection.commit()

            print()
            print("Application recorded successfully.")
            print(f"Application ID: {application_id}")
            print(f"Employer: {company_name}")
            print(f"Role: {title}")
            print("Vacancy status: Applied")

        except Exception:
            connection.rollback()
            raise


def main():
    vacancies = get_open_vacancies()

    if not vacancies:
        print("No open vacancies were found.")
        return

    display_vacancies(vacancies)

    valid_ids = {
        vacancy_id
        for vacancy_id, *_ in vacancies
    }

    vacancy_id = choose_vacancy(valid_ids)

    if vacancy_id is None:
        return

    confirmation = input(
        "\nConfirm that you submitted this application? "
        "[y/N]: "
    ).strip().lower()

    if confirmation != "y":
        print("Application was not recorded.")
        return

    try:
        apply_to_vacancy(vacancy_id)

    except ValueError as error:
        print(f"\nCould not record application: {error}")

    except Exception as error:
        print(f"\nUnexpected database error: {error}")
        raise


if __name__ == "__main__":
    main()