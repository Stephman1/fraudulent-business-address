# Use an official Python image as the base
FROM python:3.11.4-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean

# Copy requirements.txt into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory into the container
COPY backend /app/backend/
COPY address /app/address/
COPY companies_house /app/companies_house/
COPY manage.py /app/

# Expose port 8000 for the Django development server
EXPOSE 8000

# Run migrations and start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
