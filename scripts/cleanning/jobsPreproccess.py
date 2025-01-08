import pandas as pd
from src.config import SCRAPER_CONFIGS

def clean(file_path):
    """Clean the raw job postings data."""
    # Load the data
    jobs_df = pd.read_csv(file_path)

    # Drop NA values (no drop duplicate, may be necessary later)
    jobs_df = jobs_df.dropna()

    # Dropping unwanted columns is assumed to be handled during the scraping phase

    # Data cleaning for jobs_df
    # Standardize data formats

    # Clean 'salary' column, if it exists
    if 'salary' in jobs_df.columns:
        def convert_salary(value):
            """Convert salary strings to numeric values."""
            try:
                if isinstance(value, str):
                    if 'K' in value:
                        return float(value.replace('K', '')) * 1_000
                    elif 'M' in value:
                        return float(value.replace('M', '')) * 1_000_000
                return float(value)
            except ValueError:
                return None

        jobs_df['salary'] = jobs_df['salary'].apply(convert_salary)

    # Clean 'date_posted' column, if it exists
    if 'date_posted' in jobs_df.columns:
        jobs_df['date_posted'] = pd.to_datetime(jobs_df['date_posted'], errors='coerce')

    # Remove rows with invalid or missing 'Title' and 'Company'
    jobs_df = jobs_df.dropna(subset=['Title', 'Company'])

    # Remove rows with non-positive salary values (if applicable)
    if 'salary' in jobs_df.columns:
        jobs_df = jobs_df[jobs_df['salary'] > 0]

    return jobs_df
