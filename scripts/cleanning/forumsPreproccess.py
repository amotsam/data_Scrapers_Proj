import pandas as pd
from config import SCRAPER_CONFIGS

def clean(file_path):
    # Load the data
    forums_df = pd.read_csv(file_path)

    # Drop NA values
    #(no drop duplicate, maybe neccesary)
    forums_df = forums_df.dropna()

    #Dropping unwanted coulmns was done on scraping phase

    #Data cleanning for forums_df
        # Standardize data formats
    def convert_to_numeric(value):
        """Convert strings like '225.3K' or '1.5M' to numeric values."""
        try:
            if isinstance(value, str):
                if 'K' in value:
                    return float(value.replace('K', '')) * 1_000
                elif 'M' in value:
                    return float(value.replace('M', '')) * 1_000_000
            return float(value)  # Handle plain numeric strings
        except ValueError:
            return None  # Return None for invalid values

    # Apply conversion to 'Topics' and 'Messages'
    forums_df['Topics'] = forums_df['Topics'].apply(convert_to_numeric)
    forums_df['Messages'] = forums_df['Messages'].apply(convert_to_numeric)

    # Drop rows with invalid numeric values (now represented as NaN)
    forums_df = forums_df.dropna(subset=['Topics', 'Messages'])

    # Remove rows with non-positive values in numeric columns
    forums_df = forums_df[(forums_df['Topics'] > 0) & (forums_df['Messages'] > 0)]

    return forums_df
    print(f'Data cleaning completed. Cleaned dataset saved to {SCRAPER_CONFIGS["forums"]["CLEANED_OUTPUT_FILE"]}.')


