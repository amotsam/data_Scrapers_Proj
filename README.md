Data Scrapers Project

This project provides tools for web scraping, data cleaning, and uploading CSV files into a PostgreSQL database.

Features

Extract and clean data from websites.

Load CSV files into PostgreSQL.

Automatically create database tables if needed.

Setup

Install dependencies:

pip install -r requirements.txt

Update PostgreSQL credentials in the csv_to_postgres_loader.py script.

Usage

Run the scraper:

python web_scraper.py

Upload a CSV file to PostgreSQL:

python csv_to_postgres_loader.py

File Structure

scrapers/: Web scraping scripts.

db_loader/: PostgreSQL loader script.

data/: Raw and cleaned data.

License

This project is licensed under the MIT License.

Contact

GitHub: amotsam
