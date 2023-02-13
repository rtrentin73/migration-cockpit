FROM python:3.9

# Install Nginx
RUN apt-get update && apt-get install -y nginx

# Copy Nginx config
COPY nginx.conf /etc/nginx/sites-available/default

# Set up app
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port for Nginx
EXPOSE 80

# Start Nginx and Gunicorn
CMD service nginx start && gunicorn app:app -b 0.0.0.0:8000

