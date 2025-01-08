import pandas as pd


def clean(file_path):
    """Clean the raw news data."""
    # Load the data
    news_df = pd.read_csv(file_path)

    # Fill missing values
    if 'Summary' in news_df.columns:
        news_df['Summary'] = news_df['Summary'].fillna('None')
    if 'Header' in news_df.columns:
        news_df['Header'] = news_df['Header'].fillna('None')
    if 'Link' in news_df.columns:
        news_df['Link'] = news_df['Link'].fillna('None')

    # Transform the 'DateTime' column to datetime
    if 'DateTime' in news_df.columns:
        news_df['DateTime'] = pd.to_datetime(news_df['DateTime'], errors='coerce')

        # Extract year, month, day, and hour into separate columns
        news_df['Year'] = news_df['DateTime'].dt.year
        news_df['Month'] = news_df['DateTime'].dt.month
        news_df['Day'] = news_df['DateTime'].dt.day
        news_df['Hour'] = news_df['DateTime'].dt.hour

        # Remove rows where 'DateTime' couldn't be converted
        news_df = news_df.dropna(subset=['DateTime'])

    # Standardize column data (additional transformations can be added here)
    if 'Header' in news_df.columns:
        news_df['Header'] = news_df['Header'].str.strip()
    if 'Summary' in news_df.columns:
        news_df['Summary'] = news_df['Summary'].str.strip()
    if 'Link' in news_df.columns:
        news_df['Link'] = news_df['Link'].str.strip()

    # Remove rows where 'Header', 'Summary', and 'Link' are all empty or 'None'
    news_df = news_df[~((news_df['Header'] == 'None') &
                        (news_df['Summary'] == 'None') &
                        (news_df['Link'] == 'None'))]

    return news_df
