import sqlite3
from pathlib import Path


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DATABASE_PATH = Path("data/customers.db")


# ============================================================
# CREATE DATABASE
# ============================================================

def create_database():
    """
    Create the customer database and insert sample data
    if the database does not already exist.
    """

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    # --------------------------------------------------------
    # Create customers table
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            profession TEXT NOT NULL,
            segment TEXT NOT NULL,
            preferred_category TEXT NOT NULL
        )
        """
    )

    # --------------------------------------------------------
    # Check whether data already exists
    # --------------------------------------------------------

    cursor.execute(
        "SELECT COUNT(*) FROM customers"
    )

    customer_count = cursor.fetchone()[0]

    # --------------------------------------------------------
    # Insert sample customers
    # --------------------------------------------------------

    if customer_count == 0:

        customers = [
            (
                "Arjun",
                24,
                "Software Engineer",
                "Young Professionals",
                "Audio",
            ),
            (
                "Ananya",
                27,
                "UI/UX Designer",
                "Young Professionals",
                "Wearables",
            ),
            (
                "Rahul",
                31,
                "Marketing Executive",
                "Young Professionals",
                "Audio",
            ),
            (
                "Meera",
                23,
                "Data Analyst",
                "Young Professionals",
                "Wearables",
            ),
            (
                "Vishnu",
                35,
                "Product Manager",
                "Young Professionals",
                "Audio",
            ),
            (
                "Sneha",
                42,
                "Business Consultant",
                "Working Professionals",
                "Wearables",
            ),
            (
                "Akhil",
                29,
                "Software Developer",
                "Young Professionals",
                "Audio",
            ),
            (
                "Diya",
                26,
                "Graphic Designer",
                "Young Professionals",
                "Wearables",
            ),
        ]

        cursor.executemany(
            """
            INSERT INTO customers (
                name,
                age,
                profession,
                segment,
                preferred_category
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            customers,
        )

    connection.commit()
    connection.close()


# ============================================================
# CUSTOMER SEARCH
# ============================================================

def search_customers(
    segment: str | None = None,
    category: str | None = None,
    min_age: int | None = None,
    max_age: int | None = None,
) -> list[dict]:
    """
    Search customers using SQL filters.
    """

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    query = """
        SELECT
            id,
            name,
            age,
            profession,
            segment,
            preferred_category
        FROM customers
        WHERE 1 = 1
    """

    parameters = []

    # --------------------------------------------------------
    # Segment filter
    # --------------------------------------------------------

    if segment:

        query += """
            AND segment = ?
        """

        parameters.append(segment)

    # --------------------------------------------------------
    # Category filter
    # --------------------------------------------------------

    if category:

        query += """
            AND preferred_category = ?
        """

        parameters.append(category)

    # --------------------------------------------------------
    # Minimum age
    # --------------------------------------------------------

    if min_age is not None:

        query += """
            AND age >= ?
        """

        parameters.append(min_age)

    # --------------------------------------------------------
    # Maximum age
    # --------------------------------------------------------

    if max_age is not None:

        query += """
            AND age <= ?
        """

        parameters.append(max_age)

    query += """
        ORDER BY age ASC
    """

    cursor.execute(
        query,
        parameters,
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


# ============================================================
# MARKETING AUDIENCE TOOL
# ============================================================

def search_customer_audience(
    segment: str = "Young Professionals",
) -> str:
    """
    Return customer information for a marketing audience.
    """

    customers = search_customers(
        segment=segment
    )

    if not customers:
        return "No customers found."

    lines = [
        f"Customer: {customer['name']}"
        f" | Age: {customer['age']}"
        f" | Profession: {customer['profession']}"
        f" | Segment: {customer['segment']}"
        f" | Preferred Category: "
        f"{customer['preferred_category']}"
        for customer in customers
    ]

    return "\n".join(lines)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    create_database()

    print("\nCustomer Database")
    print("-----------------")

    customers = search_customers(
        segment="Young Professionals"
    )

    for customer in customers:

        print(
            f"{customer['name']} | "
            f"{customer['age']} | "
            f"{customer['profession']} | "
            f"{customer['preferred_category']}"
        )

    print("\nMarketing Audience")
    print("------------------")

    print(
        search_customer_audience(
            "Young Professionals"
        )
    )