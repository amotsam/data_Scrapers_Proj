import pandas as pd


def transform(file_path):
    """Transform the cleaned news data."""
    try:
        # Load the cleaned data
        data = pd.read_csv(file_path)
        print("Data loaded successfully. Ready for transformation.")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}. Please check the file path.")
        raise
    except Exception as e:
        print(f"Error loading the file: {e}")
        raise

    try:
        # Define the average reading speed (words per second)
        AVERAGE_WPM = 250  # Average words per minute
        AVERAGE_WPS = AVERAGE_WPM / 60  # Words per second

        # Add estimated reading time for the 'Summary' column
        if 'Summary' in data.columns:
            def calculate_reading_time(text):
                if pd.isnull(text):
                    return None  # Handle missing summaries
                word_count = len(text.split())
                return round(word_count / AVERAGE_WPS)  # Calculate time in seconds

            data['estimated_reading_time_seconds'] = data['Summary'].apply(calculate_reading_time)
            print("Estimated reading time added successfully.")
        else:
            raise KeyError("The column 'Summary' does not exist in the dataset.")

        # Add segmentation based on reading time
        if 'estimated_reading_time_seconds' in data.columns:
            labels = ['Short', 'Medium', 'Long', 'Very Long']
            data['reading_time_segment'] = pd.cut(
                data['estimated_reading_time_seconds'],
                bins=4,
                labels=labels,
                include_lowest=True
            )
            print("Reading time segmentation applied successfully.")

    except Exception as e:
        print(f"Error during transformation: {e}")
        raise

    # Return the transformed data
    return data
