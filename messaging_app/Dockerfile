# Use lightweight Python
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed to build Python packages and MySQL client
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    python3-dev \
    pkg-config \
    netcat-traditional \
    default-mysql-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Expose Django port
EXPOSE 8000

# Run Django server
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
