import logging
import pandas as pd

def clean(file_path):
    """Clean and preprocess the shopping data."""
    # Load the dataset
    try:
        products_data = pd.read_csv(file_path)
        logging.info("Data loaded successfully.")
    except FileNotFoundError:
        logging.error(f"Error: File not found at {file_path}. Please check the file path.")
        raise
    except Exception as e:
        logging.error(f"Error loading the file: {e}")
        raise

    # Remove duplicates
    products_cleaned = products_data.drop_duplicates()

    # Function to split price ranges into individual rows
    def expand_price_ranges(df):
        expanded_rows = []
        for _, row in df.iterrows():
            price = row['Price'].strip()  # Remove leading/trailing spaces
            if '–' in price:  # Check for range delimiter
                try:
                    # Split and clean each price value before conversion
                    prices = price.split('–')
                    low = float(prices[0].replace('₪', '').replace(',', '').strip())
                    high = float(prices[1].replace('₪', '').replace(',', '').strip())

                    row_low = row.copy()
                    row_low['Price'] = low
                    expanded_rows.append(row_low)

                    row_high = row.copy()
                    row_high['Price'] = high
                    expanded_rows.append(row_high)
                except ValueError as e:
                    logging.error(f"Failed to process price range: {price}. Error: {str(e)}")
            else:
                try:
                    row['Price'] = float(price.replace('₪', '').replace(',', '').strip())
                    expanded_rows.append(row)
                except ValueError as e:
                    logging.error(f"Failed to convert price: {price}. Error: {str(e)}")

        return pd.DataFrame(expanded_rows)

    # Apply the function to handle price ranges and clean the Price column
    try:
        products_cleaned = expand_price_ranges(products_cleaned)
        products_cleaned.reset_index(drop=True, inplace=True)
        logging.info("Price ranges expanded and cleaned successfully.")
    except Exception as e:
        logging.error(f"Error while processing price ranges: {str(e)}")
        raise

    return products_cleaned
