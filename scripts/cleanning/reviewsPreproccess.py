import pandas as pd

def clean(file_path):
    """Clean and preprocess the reviews data."""
    # Load the data
    reviews_df = pd.read_csv(file_path)

    # Remove duplicates based on movie name, review text, and rating
    reviews_df = reviews_df.drop_duplicates(subset=['Movie', 'Review', 'Rating'], keep='first')

    # Standardize column names (convert to lowercase and replace spaces with underscores)
    reviews_df.columns = [col.lower().replace(" ", "_") for col in reviews_df.columns]

    # Strip extra spaces from text columns
    reviews_df['movie'] = reviews_df['movie'].str.strip()
    reviews_df['review'] = reviews_df['review'].str.strip()
    reviews_df['rating'] = reviews_df['rating'].str.strip()

    # Ensure the 'rating' column is clean (remove unnecessary characters like "/10")
    reviews_df['rating'] = reviews_df['rating'].str.extract(r'(\d+)').astype(float)

    return reviews_df
