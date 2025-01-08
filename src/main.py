import logging
import utils as utils
from config import SCRAPER_CONFIGS
from importlib import import_module
import data_loader


def loginng():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def validate_data(file_path, validation_rules):
    """Validate data against defined rules."""
    import pandas as pd
    try:
        data = pd.read_csv(file_path)
        # Check required columns
        for col in validation_rules.get("required_columns", []):
            if col not in data.columns:
                logging.error(f"Validation failed: Missing column '{col}' in {file_path}")
                return False
        # Check non-empty columns
        for col in validation_rules.get("non_empty_columns", []):
            if data[col].isnull().any():
                logging.error(f"Validation failed: Column '{col}' contains empty values in {file_path}")
                return False
        logging.info(f"Validation passed for {file_path}")
        return True
    except Exception as e:
        logging.error(f"Error during validation for {file_path}: {e}")
        return False


def run_scraper(domain):
    """Run the scraping and processing pipeline for a specific domain."""
    logging.info(f"Starting pipeline for {domain}...")
    try:
        config = SCRAPER_CONFIGS[domain]
        session = utils.Init_session()

        # Dynamically import scraper module
        scraper_module = import_module(f"scripts.scrapers.{domain}Scraper")

        # Scrape raw data
        html_scraped = utils.fetch_html(config["BASE_URL"], session,domain)

        if not html_scraped:
            raise RuntimeError(f"Scraping failed for {domain}")
        # Parse
        if hasattr(scraper_module, "parse_data"):
            raw_data = scraper_module.parse_data(html_scraped)
            utils.save_to_csv(raw_data, config["RAW_OUTPUT_FILE"])

            # Validate scraped data
            if not validate_data(config["RAW_OUTPUT_FILE"], config["validation"]["scraped"]):
                raise ValueError(f"Validation failed for scraped data in {domain}")

        else:
            raise AttributeError(f"'parse_data' function not found in {domain}Scraper")

        # Clean data
        cleaner_module = import_module(f"scripts.cleanning.{domain}Preproccess")
        cleaned_data = cleaner_module.clean(config["RAW_OUTPUT_FILE"])
        utils.save_to_csv(cleaned_data, config["TRANSFORMED_OUTPUT_FILE"])

        # Transform data
        transformer_module = import_module(f"scripts.transformation.{domain}_feature_eng")
        transformed_data = transformer_module.transform(config["TRANSFORMED_OUTPUT_FILE"])
        utils.save_to_csv(transformed_data, config["TRANSFORMED_OUTPUT_FILE"])

        # Validate transformed data
        if not validate_data(config["TRANSFORMED_OUTPUT_FILE"], config["validation"]["transformed"]):
            raise ValueError(f"Validation failed for transformed data in {domain}")

        logging.info(f"Pipeline for {domain} completed successfully.")
    except Exception as e:
        logging.error(f"Error in pipeline for {domain}: {e}")


def load_data_to_db():
    """Load data from cleaned CSVs into the database."""
    logging.info("Starting data loading into PostgreSQL...")
    try:
        data_loader.process_all_tables()
        logging.info("Data loading completed successfully.")
    except Exception as e:
        logging.error(f"Error during data loading: {e}")


def main():
    """Main function to orchestrate scraping and data loading."""
    loginng()
    logging.info("Starting scraping and data loading project...")

    # Run scraping and processing for all domains
    for domain in SCRAPER_CONFIGS["ALL_DOMAINS"]:
        try:
            run_scraper(domain)
        except Exception as e:
            logging.error(f"Failed to process domain {domain}: {e}")

    # Load cleaned data into PostgreSQL
    load_data_to_db()

    logging.info("All tasks completed.")


if __name__ == "__main__":
    main()
