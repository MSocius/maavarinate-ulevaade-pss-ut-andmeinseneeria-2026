FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y cron

# Install Python dependencies if needed
# RUN pip install -r requirements.txt

# Copy crontab file
COPY crontab.txt /etc/cron.d/app-cron

# Give execution rights
RUN chmod 0644 /etc/cron.d/app-cron

# Apply cron job
RUN crontab /etc/cron.d/app-cron

CMD ["cron", "-f"]
