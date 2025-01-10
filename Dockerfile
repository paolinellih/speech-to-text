# Use the official Python image as the base image
FROM python:3.9-slim

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    portaudio19-dev \
    ffmpeg \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Copy the wait-for-it.sh script into the container
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Copy init_db.py to the container
COPY init_db.py /app/init_db.py

# Expose the port for the FastAPI app
EXPOSE 8000

# Add entrypoint script
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Run the FastAPI app with entrypoint script
CMD ["/app/docker-entrypoint.sh"]
