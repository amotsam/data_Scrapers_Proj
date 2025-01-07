import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

# File paths of uploaded files
file_paths = [
    '../../data/transformed/transformed_forums_data.csv',
    '../../data/transformed/transformed_jobs_data.csv',
    '../../data/transformed/transformed_news_data.csv',
    '../../data/transformed/transformed_review_data.csv',
    '../../data/transformed/transformed_shopping.csv'
]

# Load all data and combine text columns
combined_texts = []

for file_path in file_paths:
    try:
        df = pd.read_csv(file_path)
        # Combine all text columns in the dataset
        text_columns = df.select_dtypes(include=['object']).columns
        combined_texts.extend(df[text_columns].fillna("").values.flatten())
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Combine all texts into a single corpus
corpus = " ".join(combined_texts)

# Extract unigrams, bigrams, and trigrams
results = {}
for ngram_range, header in [((1, 1), "unigram"), ((2, 2), "bigram"), ((3, 3), "trigram")]:
    vectorizer = CountVectorizer(ngram_range=ngram_range, max_features=20)
    X = vectorizer.fit_transform([corpus])
    features = vectorizer.get_feature_names_out()
    # Exclude single-word entries for bigrams and trigrams
    if ngram_range != (1, 1):
        features = [feature for feature in features if len(feature.split()) == ngram_range[1]]
    results[header] = features

# Display the results as an array of documents
results_array = [{"header": header, "values": list(values)} for header, values in results.items()]

# Print the structured results
print(results_array)
