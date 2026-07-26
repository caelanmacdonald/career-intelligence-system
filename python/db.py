import os

import psycopg
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection() -> psycopg.Connection:
    """Create and return a connection to the PostgreSQL database."""

    if not DATABASE_URL:
        raise ValueError(
            "DATABASE_URL was not found. Add it to the project's .env file."
        )

    return psycopg.connect(DATABASE_URL)


def test_connection() -> None:
    """Test the database connection and print basic database information."""

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    current_database(),
                    current_user,
                    CURRENT_TIMESTAMP;
                """
            )

            database_name, database_user, database_time = cursor.fetchone()

    print("Database connection successful.")
    print(f"Database: {database_name}")
    print(f"User: {database_user}")
    print(f"Server time: {database_time}")


if __name__ == "__main__":
    test_connection()