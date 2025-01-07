
import pandas as pd


# Forums domain
# User active grade
# Load the data

def transform(file_path):
    try:
        # Load the data
        data = pd.read_csv(file_path)
        print("Data loaded successfully ready to transform.")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}. Please check the file path.")
        raise
    except Exception as e:
        print(f"Error loading the file: {e}")
        raise

    try:
        # Calculate 'usersActiveGrade' if it doesn't exist
        if 'usersActiveGrade' not in data.columns:
            if 'Messages' in data.columns and 'Topics' in data.columns:
                data['usersActiveGrade'] = (data['Messages'] / data['Topics']).fillna(0).astype(float)
                print("'usersActiveGrade' column created successfully.")
            else:
                raise KeyError(
                    "The dataset must contain 'Messages' and 'Topics' columns to calculate 'usersActiveGrade'.")

        # Define the activity labels
        activity_labels = ['little activity', 'medium activity', 'active', 'very active']

        # Create bins for the segments excluding 0
        non_zero_bins = pd.cut(
            data.loc[data['usersActiveGrade'] > 0, 'usersActiveGrade'],
            bins=4,  # Divide into 4 segments for non-zero values
            labels=activity_labels,
            include_lowest=True
        )

        # Assign "no activity" to rows where usersActiveGrade is 0
        data['activityLevel'] = 'no activity'
        data.loc[data['usersActiveGrade'] > 0, 'activityLevel'] = non_zero_bins

        print("Segmentation successfully applied.")

    except KeyError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"Error during segmentation: {e}")
        raise

    # Return the transformed data
    return data
