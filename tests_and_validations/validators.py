import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def validate_columns(data, required_columns):
    """Validate if all required columns are present."""
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        logging.error(f"Missing columns: {missing_columns}")
        return False
    return True


def validate_non_empty_columns(data, columns):
    """Check if specified columns contain non-empty values."""
    for column in columns:
        if data[column].isnull().any():
            logging.error(f"Null values found in column: {column}")
            return False
    return True


def validate_data_types(data, column_types):
    """Check if columns have the expected data types."""
    for column, dtype in column_types.items():
        if column not in data.columns:
            logging.warning(f"Skipping type check for missing column: {column}")
            continue
        if not pd.api.types.is_dtype_equal(data[column].dtype, dtype):
            logging.error(f"Incorrect data type for column {column}. Expected {dtype}, got {data[column].dtype}")
            return False
    return True


def validate_value_ranges(data, column, valid_range):
    """Validate if values in a column fall within a valid range."""
    if not data[column].between(*valid_range).all():
        logging.error(f"Values in column {column} fall outside the valid range: {valid_range}")
        return False
    return True


def validate_categorization(data, column, valid_categories):
    """Validate if values in a column match a list of valid categories."""
    if not data[column].isin(valid_categories).all():
        logging.error(f"Invalid values found in column {column}.")
        return False
    return True


def validate_scraped_data(file_path, domain_config):
    """Run validation checks for scraped data."""
    try:
        data = pd.read_csv(file_path)
        logging.info(f"Validating scraped data: {file_path}")

        # Validate columns
        if not validate_columns(data, domain_config["required_columns"]):
            return False

        # Validate non-empty critical columns
        if not validate_non_empty_columns(data, domain_config["non_empty_columns"]):
            return False

        # Validate data types
        if not validate_data_types(data, domain_config["data_types"]):
            return False

        return True
    except Exception as e:
        logging.error(f"Error validating scraped data: {e}")
        return False


def validate_transformed_data(file_path, domain_config):
    """Run validation checks for transformed data."""
    try:
        data = pd.read_csv(file_path)
        logging.info(f"Validating transformed data: {file_path}")

        # Validate columns
        if not validate_columns(data, domain_config["required_columns"]):
            return False

        # Validate categorization
        if "categorization" in domain_config:
            for column, categories in domain_config["categorization"].items():
                if not validate_categorization(data, column, categories):
                    return False

        return True
    except Exception as e:
        logging.error(f"Error validating transformed data: {e}")
        return False
