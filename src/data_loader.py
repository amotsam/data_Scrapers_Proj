import logging
import psycopg2
import pandas as pd
from importlib import import_module

# Database configuration
DB_CONFIG = {
    "host": "localhost",         # Change to your PostgreSQL host
    "database": "Domains_data",  # Change to your database name
    "user": "postgres",          # Change to your database user
    "password": "admin",         # Change to your database password
    "port": 5432                 # PostgreSQL port
}

# Tables and CSV files configuration
TABLE_CONFIGS = {
    "forums": "../data/cleaned/cleaned_forums_data.csv",
    "products": "../data/cleaned/cleaned_jobs_data.csv",
    "news": "../data/cleaned/cleaned_news_data.csv",
    "reviews": "../data/cleaned/cleaned_review_data.csv",
    "shopping": "../data/cleaned/cleaned_shopping_data.csv"
}

def connect_to_db():
    """Connect to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logging.info("Connected to the database successfully.")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")
        return None


def create_table_if_not_exists(conn, table_name, columns):
    """Create a table if it does not exist."""
    try:
        column_definitions = ", ".join([f"{col} TEXT" for col in columns])
        create_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {column_definitions}
        );
        """
        with conn.cursor() as cur:
            cur.execute(create_query)
            conn.commit()
        logging.info(f"Table '{table_name}' is ready.")
    except Exception as e:
        logging.error(f"Failed to create table {table_name}: {e}")
        conn.rollback()


def load_csv_to_db(conn, table_name, file_path):
    """Load a CSV file into the PostgreSQL database."""
    try:
        # Load the CSV file using pandas
        df = pd.read_csv(file_path)

        # Convert DataFrame to a list of tuples for insertion
        records = df.to_dict(orient="records")
        columns = df.columns.tolist()
        placeholders = ", ".join(["%s"] * len(columns))

        insert_query = f"""
        INSERT INTO {table_name} ({', '.join(columns)})
        VALUES ({placeholders})
        """

        with conn.cursor() as cur:
            for record in records:
                cur.execute(insert_query, tuple(record.values()))
            conn.commit()

        logging.info(f"Loaded {len(df)} rows from {file_path} into {table_name}.")
    except Exception as e:
        logging.error(f"Failed to load CSV into database: {e}")
        conn.rollback()


def process_table(table_name, file_path, conn):
    """Process each table by loading its associated CSV."""
    logging.info(f"Processing table: {table_name} from file: {file_path}")
    try:
        # Load the CSV file to determine its columns
        df = pd.read_csv(file_path)

        # Create table if it does not exist
        create_table_if_not_exists(conn, table_name, df.columns)

        # Load data into the table
        load_csv_to_db(conn, table_name, file_path)

    except Exception as e:
        logging.error(f"Error processing table {table_name}: {e}")


def setup_logging():
    """Set up logging for the script."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def process_all_tables():
    """Process all tables and load the respective CSVs into the database."""
    setup_logging()

    conn = connect_to_db()
    if not conn:
        logging.error("Database connection failed. Exiting.")
        return

    try:
        for table_name, file_path in TABLE_CONFIGS.items():
            process_table(table_name, file_path, conn)
    finally:
        conn.close()
        logging.info("Database connection closed.")
