import pandas as pd
import re

def transform(file_path):
    """Perform feature engineering for jobs data."""
    try:
        # Load the cleaned data
        data = pd.read_csv(file_path)
        print("Data loaded successfully.")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}. Please check the file path.")
        raise
    except Exception as e:
        print(f"Error loading the file: {e}")
        raise

    # Define job names
    job_names = {"מחסנאי", "נציג", "מלקט", "שומר", "מאבטח", "מהנדס", "ארכיטקט", "מתכנת", "קופאי", "מכונאי", "סדרן"}

    # Extract job names based on the predefined set
    def extract_job_name(title):
        for job in job_names:
            if re.search(rf"\b{job}\b", title):
                return job
        return "UNKNOWN"

    # Add the 'job_name' column
    if 'Title' in data.columns:
        data['job_name'] = data['Title'].apply(extract_job_name)
        print("Job names extracted successfully.")
    else:
        raise KeyError("The column 'Title' does not exist in the dataset.")

    # Return the transformed data
    return data
