"""Query the 'mock' table in the bqn6bm_mock database."""

import logging
import os

import mysql.connector

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Credentials come from environment variables
DBHOST = os.environ.get("DBHOST")
DBNAME = os.environ.get("DBNAME")
DBUSER = os.environ.get("DBUSER")
DBPASS = os.environ.get("DBPASS")


def get_connection():
    """Open and return a MySQL connection using env var credentials."""
    return mysql.connector.connect(
        host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME
    )


def get_data_by_group(value):
    """Return all rows from mock where the `group` column equals value.

    Filter column: `group` (backticked because GROUP is reserved in MySQL).

    Args:
        value: the group value to match.
    Returns:
        list of row tuples (empty list on error).
    """
    query = "SELECT * FROM mock WHERE `group` = %s"  # %s is a placeholder
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (value,))  # tuple, not a bare value
        rows = cursor.fetchall()
        logging.info("Found %d rows for group %s", len(rows), value)
        return rows
    except mysql.connector.Error as err:
        logging.error("Database error: %s", err)
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def plot_counts(groupby):
    """Count rows per distinct value of a column.

    Args:
        groupby: name of a column in the mock table.
    Returns:
        list of (value, count) tuples (empty list on error).
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Identifiers can't be parameterized, so validate against real column names
        cursor.execute("SHOW COLUMNS FROM mock")
        valid_cols = [r[0] for r in cursor.fetchall()]
        if groupby not in valid_cols:
            logging.error("Unknown column: %s", groupby)
            return []

        query = (
            f"SELECT `{groupby}`, COUNT(*) FROM mock "
            f"GROUP BY `{groupby}` ORDER BY COUNT(*) DESC"
        )
        cursor.execute(query)
        counts = cursor.fetchall()
        logging.info("Got %d distinct values for %s", len(counts), groupby)
        return counts
    except mysql.connector.Error as err:
        logging.error("Database error: %s", err)
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def main():
    """Demonstrate the query functions."""
    # Count rows per group first, then use the biggest group for the filter demo
    counts = plot_counts("group")
    print("Counts per group:")
    for value, count in counts:
        print(value, count)

    if counts:
        top_group = counts[0][0]
        print(f"\nRows in group '{top_group}':")
        for row in get_data_by_group(top_group):
            print(row)


if __name__ == "__main__":
    main()
