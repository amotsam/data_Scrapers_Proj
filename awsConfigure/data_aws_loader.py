import pandas as pd
import boto3

# AWS Redshift connection parameters
cluster_id = 'your-cluster-id'  # Replace with your Redshift Cluster ID
db_name = 'dev'  # Replace with your Redshift database name
db_user = 'awsuser'  # Replace with your Redshift user
db_password = 'password'  # Replace with your Redshift password
db_host = f'{cluster_id}.cluster-region.redshift.amazonaws.com'  # Example: 'your-cluster.cluster-region.redshift.amazonaws.com'

# S3 bucket for Redshift
s3_bucket = 'your-s3-bucket'  # Replace with your S3 bucket name


# Function to upload CSV to S3
def upload_to_s3(file_path, bucket, object_name):
    s3_client = boto3.client('s3')
    s3_client.upload_file(file_path, bucket, object_name)


# File paths
csv_files = [
    '../data/cleaned/cleaned_shopping_data.csv',
    '../data/cleaned/cleaned_review_data.csv',
    '../data/cleaned/cleaned_news_data.csv',
    '../data/cleaned/cleaned_jobs_data.csv',
    '../data/cleaned/cleaned_forums_data.csv'
]


# Step 2: Load data into Redshift
def load_csv_to_redshift(file_path, table_name):
    upload_to_s3(file_path, s3_bucket, f'redshift_data/{table_name}.csv')

    # Redshift SQL Query
    create_table_query = f'''
    CREATE TABLE {table_name} (
        -- Define columns and data types
        column1 datatype,
        column2 datatype,
        column3 datatype,
        -- Add all other columns
    );
    '''

    # Connect to Redshift
    redshift_conn = boto3.client('redshift-data')

    # Load data into Redshift table
    copy_query = f'''
    COPY {table_name} 
    FROM 's3://{s3_bucket}/redshift_data/{table_name}.csv' 
    IAM_ROLE 'arn:aws:iam::account_id:role/RedshiftS3Access' 
    CSV;
    '''

    # Execute the queries
    redshift_conn.execute_statement(
        ClusterIdentifier=cluster_id,
        Database=db_name,
        DbUser=db_user,
        Sql=create_table_query + copy_query
    )

# Step 3: Process each file
for file_path in csv_files:
    table_name = file_path.split('/')[-1].replace('.csv', '')
    load_csv_to_redshift(file_path, table_name)

################# creating tables with glue
