FROM python:3.9

# Install Docker
RUN apt-get update && apt-get install ca-certificates curl gnupg lsb-release -y
RUN mkdir -m 0755 -p /etc/apt/keyrings && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update && apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Install Google Cloud 
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-cli -y
      
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
EXPOSE 8080

# Start Nginx and Gunicorn
CMD service docker start && service nginx start && gunicorn cockpit:app -b 0.0.0.0:8080

# Set up GCR authentication
ARG GCP_PROJECT_ID
ARG GCP_SA_KEY

RUN echo ${GCP_SA_KEY} | base64 -d > /tmp/gcp_sa_key.json && \
    gcloud auth activate-service-account --key-file=/tmp/gcp_sa_key.json && \
    gcloud auth configure-docker && \
    rm -rf /tmp/gcp_sa_key.json

# Tag and upload the Docker image to GCR
# ARG IMAGE_NAME
# RUN docker build -t ${IMAGE_NAME} .
# RUN docker tag ${IMAGE_NAME} gcr.io/${GCP_PROJECT_ID}/${IMAGE_NAME}:latest
# RUN docker push gcr.io/${GCP_PROJECT_ID}/${IMAGE_NAME}:latest