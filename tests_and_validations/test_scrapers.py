from tests_and_validations.validators import validate_scraped_data, validate_transformed_data

# Configuration for validation
DOMAIN_VALIDATION_CONFIGS = {
    "shopping": {
        "scraped": {
            "file_path": "../../data/rawData/shopping_products.csv",
            "required_columns": ["Name", "Price", "Rating", "Categories"],
            "non_empty_columns": ["Name", "Price"],
            "data_types": {"Price": float},
        },
        "transformed": {
            "file_path": "../../data/transformed/transformed_shopping_data.csv",
            "required_columns": ["Extracted_Product_Name", "Price_Category"],
            "categorization": {
                "Price_Category": ["Low", "Medium", "High", "Premium"],
            },
        },
    },
    "forums": {
        "scraped": {
            "file_path": "../../data/rawData/forums_data.csv",
            "required_columns": ["User", "Messages", "Topics"],
            "non_empty_columns": ["User", "Messages"],
            "data_types": {"Messages": int, "Topics": int},
        },
        "transformed": {
            "file_path": "../../data/transformed/transformed_forums_data.csv",
            "required_columns": ["usersActiveGrade"],
        },
    },
    # Add other domain configurations (news, reviews, jobs) here
}


def test_scraped_data():
    """Test validation of scraped data for all domains."""
    for domain, configs in DOMAIN_VALIDATION_CONFIGS.items():
        print(f"Testing scraped data for domain: {domain}")
        if not validate_scraped_data(configs["scraped"]["file_path"], configs["scraped"]):
            print(f"Validation failed for scraped data in domain: {domain}")
        else:
            print(f"Validation passed for scraped data in domain: {domain}")


def test_transformed_data():
    """Test validation of transformed data for all domains."""
    for domain, configs in DOMAIN_VALIDATION_CONFIGS.items():
        print(f"Testing transformed data for domain: {domain}")
        if not validate_transformed_data(configs["transformed"]["file_path"], configs["transformed"]):
            print(f"Validation failed for transformed data in domain: {domain}")
        else:
            print(f"Validation passed for transformed data in domain: {domain}")



