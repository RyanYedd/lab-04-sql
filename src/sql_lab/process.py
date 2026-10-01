"""Read, clean, and load MOCK_DATA.csv into the MySQL 'mock' table."""

import logging
import os

import mysql.connector
import pandas as pd

# Configure logging so each function can report status
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Read connection settings from environment variables
DBHOST = os.environ.get("DBHOST")
DBNAME = os.environ.get("DBNAME")
DBUSER = os.environ.get("DBUSER")
DBPASS = os.environ.get("DBPASS")

# Map pandas dtypes to SQL types
TYPE_MAPPING = {
    "int64": "BIGINT",
    "int32": "INT",
    "float64": "DOUBLE",
    "bool": "TINYINT(1)",
    "datetime64[ns]": "DATETIME",
    "object": "VARCHAR(255)",
    "string": "VARCHAR(255)",
}


def read_data(filename):
    """Load a CSV file into a DataFrame.

    Args:
        filename: path to the CSV file.
    Returns:
        pandas DataFrame with the file contents.
    """
    logging.info("Reading %s", filename)
    data = pd.read_csv(filename)
    logging.info("Read %d rows, %d columns", data.shape[0], data.shape[1])
    return data


def clean_data(data):
    """Remove rows with missing values.

    Args:
        data: raw DataFrame.
    Returns:
        cleaned DataFrame with no missing values.
    """
    cleaned = data.dropna().reset_index(drop=True)
    logging.info("Dropped %d rows with missing values", len(data) - len(cleaned))
    return cleaned


def load_data(data, table):
    """Create the table if needed and insert the DataFrame row by row.

    Args:
        data: cleaned DataFrame.
        table: destination table name (use "mock").
    """
    # Build column definitions from dtypes; backticks protect reserved words like `group`
    col_defs = ", ".join(
        f"`{col}` {TYPE_MAPPING.get(str(dtype), 'VARCHAR(255)')}"
        for col, dtype in data.dtypes.items()
    )
    create_sql = f"CREATE TABLE IF NOT EXISTS `{table}` ({col_defs})"

    # Column names/placeholders are built from the DataFrame; VALUES use %s placeholders
    cols = ", ".join(f"`{c}`" for c in data.columns)
    placeholders = ", ".join(["%s"] * len(data.columns))
    insert_sql = f"INSERT INTO `{table}` ({cols}) VALUES ({placeholders})"

    conn = None
    try:
        conn = mysql.connector.connect(
            host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME
        )
        cursor = conn.cursor()
        cursor.execute(create_sql)
        # Clear old rows so reruns don't create duplicates
        cursor.execute(f"TRUNCATE TABLE `{table}`")

        # astype(object) converts numpy types to plain Python types
        for row in data.astype(object).itertuples(index=False, name=None):
            cursor.execute(insert_sql, tuple(row))

        conn.commit()
        logging.info("Inserted %d rows into %s", len(data), table)
    except mysql.connector.Error as err:
        logging.error("Database error: %s", err)
        if conn:
            conn.rollback()
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            logging.info("Connection closed")


def main():
    """Run the read -> clean -> load pipeline."""
    data = read_data("MOCK_DATA.csv")
    data = clean_data(data)
    load_data(data, "mock")


if __name__ == "__main__":
    main()
