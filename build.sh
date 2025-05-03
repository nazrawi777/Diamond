#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting deployment script for Render..."

# Step 1: Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Step 2: Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Step 3: Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Deployment completed successfully on Render!"
