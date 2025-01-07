import os
import pandas as pd

def transform(file_path):
    """Perform feature engineering on the cleaned review data."""
    try:
        # Load the dataset
        data = pd.read_csv(file_path)
        print("Data loaded successfully.")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}. Please check the file path.")
        raise
    except Exception as e:
        print(f"Error loading the file: {e}")
        raise

    # Define Hebrew sentiment word lists
    positive_words = ["מדהים", "טוב", "מצוין", "יפה", "נהדר", "מעולה"]
    negative_words = ["רע", "גרוע", "מאכזב", "אכזבה", "זוועה", "נורא"]

    # Function to analyze sentiment using rule-based approach
    def analyze_sentiment(text):
        try:
            if any(word in text for word in positive_words):
                return "POSITIVE"
            elif any(word in text for word in negative_words):
                return "NEGATIVE"
            return "NEUTRAL"
        except Exception as e:
            print(f"Error analyzing text: {text}\nError: {e}")
            return "ERROR"

    # Apply sentiment analysis to the 'review' column
    if 'review' in data.columns:
        try:
            data['user_feeling'] = data['review'].apply(analyze_sentiment)
            print("Sentiment analysis applied successfully.")
        except Exception as e:
            print(f"Error applying sentiment analysis: {e}")
            raise
    else:
        raise KeyError("The column 'review' does not exist in the dataset.")

    return data
