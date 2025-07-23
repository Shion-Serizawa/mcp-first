FROM python:3.12-slim

WORKDIR /app

# Install MySQL client
RUN apt-get update && \
    apt-get install -y default-mysql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set default environment variables
ENV MYSQL_HOST=localhost \
    MYSQL_PORT=3306 \
    MYSQL_USER=root \
    MYSQL_PASSWORD=password \
    MYSQL_DATABASE=information_schema

# Expose the port the server runs on
EXPOSE 8000

# Command to run the server
CMD ["python", "main.py"]
