import boto3

# AWS Glue Client
glue_client = boto3.client('glue')

# Database Name
database_name = 'my_redshift_database'  # Replace with your database name

# List of CSV files
csv_files = [
    's3://your-s3-bucket/path/cleaned_shopping_data.csv',
    's3://your-s3-bucket/path/cleaned_review_data.csv',
    's3://your-s3-bucket/path/cleaned_news_data.csv',
    's3://your-s3-bucket/path/cleaned_jobs_data.csv',
    's3://your-s3-bucket/path/cleaned_forums_data.csv'
]

# Create a Glue Database
glue_client.create_database(DatabaseInput={
    'Name': database_name,
    'Description': 'Database for Redshift tables',
})

# Create Crawlers for each CSV file
for file_path in csv_files:
    table_name = file_path.split('/')[-1].replace('.csv', '')
    glue_client.create_crawler(
        CrawlerName=f'{table_name}_crawler',
        Role='AWSGlueServiceRole',  # Replace with your Glue Service Role
        DatabaseName=database_name,
        Targets={
            'S3Targets': [
                {
                    'Path': file_path
                }
            ]
        },
        TablePrefix=table_name
    )

# Run Crawlers
for file_path in csv_files:
    table_name = file_path.split('/')[-1].replace('.csv', '')
    glue_client.start_crawler(Name=f'{table_name}_crawler')

############loadTablestoredshift

import boto3

# AWS Glue Client
glue_client = boto3.client('glue')

# Database Name
database_name = 'my_redshift_database'  # Replace with your database name

# List of CSV files
csv_files = [
    's3://your-s3-bucket/path/cleaned_shopping_data.csv',
    's3://your-s3-bucket/path/cleaned_review_data.csv',
    's3://your-s3-bucket/path/cleaned_news_data.csv',
    's3://your-s3-bucket/path/cleaned_jobs_data.csv',
    's3://your-s3-bucket/path/cleaned_forums_data.csv'
]

# Create a Glue Database
glue_client.create_database(DatabaseInput={
    'Name': database_name,
    'Description': 'Database for Redshift tables',
})

# Create Crawlers for each CSV file
for file_path in csv_files:
    table_name = file_path.split('/')[-1].replace('.csv', '')
    glue_client.create_crawler(
        CrawlerName=f'{table_name}_crawler',
        Role='AWSGlueServiceRole',  # Replace with your Glue Service Role
        DatabaseName=database_name,
        Targets={
            'S3Targets': [
                {
                    'Path': file_path
                }
            ]
        },
        TablePrefix=table_name
    )

# Run Crawlers
for file_path in csv_files:
    table_name = file_path.split('/')[-1].replace('.csv', '')
    glue_client.start_crawler(Name=f'{table_name}_crawler')

