Data Scrapers Project

This project provides tools for web scraping, data cleaning, and uploading CSV files into a PostgreSQL database.

Features

Extract and clean data from websites.

Load CSV files into PostgreSQL.

Automatically create database tables if needed.

Setup
Build and Run the Docker Container:

To set up the project, use Docker to build and run the container. The container will automatically execute the src/main.py file, and you can view the logs in real-time as it runs.

bash
Copy code
docker build -t my_image_name . && docker run --rm -it my_image_name

docker build -t my_image_name .: Builds the Docker image and tags it as my_image_name.
docker run --rm -it my_image_name: Runs the Docker container interactively and removes it after it stops.
Logs: The logs from src/main.py will be displayed in your terminal.

Configuration

PostgreSQL Credentials:
Update the PostgreSQL credentials in config.json or as environment variables in the Dockerfile, depending on your setup.
Dependencies:

All required dependencies are installed automatically in the Docker image using the requirements.txt file.





Contact

GitHub: amotsam
