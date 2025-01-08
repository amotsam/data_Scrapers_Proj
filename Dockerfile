# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add src to PYTHONPATH
ENV PYTHONPATH=/app

# Copy the rest of the application code into the container
COPY . .

# Expose a port (if needed) and set the default command
CMD ["python", "src/main.py"]
