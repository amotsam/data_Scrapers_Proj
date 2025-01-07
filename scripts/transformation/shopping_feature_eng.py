import pandas as pd

def transform(file_path):
    """Perform feature engineering on the shopping data."""
    try:
        # Load the dataset
        data = pd.read_csv(file_path)
        print("Data loaded successfully, ready to transform.")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}. Please check the file path.")
        raise
    except Exception as e:
        print(f"Error loading the file: {e}")
        raise

    try:
        # Ensure the 'Name' and 'Price' columns exist
        if 'Name' not in data.columns or 'Price' not in data.columns:
            raise KeyError("The dataset must contain 'Name' and 'Price' columns.")

        # Extract product categories if not already present
        if 'Extracted_Product_Name' not in data.columns:
            # Extract a single descriptive word from the 'Name' column
            data['Extracted_Product_Name'] = data['Name'].apply(lambda x: x.split()[0] if isinstance(x, str) else "Unknown")
            print("'Extracted_Product_Name' column created successfully.")

        # Categorize products based on price
        if 'Price_Category' not in data.columns:
            data['Price_Category'] = pd.cut(
                data['Price'],
                bins=[0, 100, 500, 1000, float('inf')],
                labels=['Low', 'Medium', 'High', 'Premium'],
                right=False
            )
            print("'Price_Category' column created successfully.")

    except KeyError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"Error during feature engineering: {e}")
        raise

    # Return the transformed data
    return data
