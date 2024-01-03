#!/bin/bash

# Stop all existing gunicorn processes
pkill gunicorn

# Wait for existing processes to be terminated
sleep 5

# Remove old directories
rm -rf /home/ubuntu/gunicorn.log
rm -rf /home/ubuntu/ssgAdminBE

# Create a new directory
mkdir /home/ubuntu/ssgAdminBE

# Start a single gunicorn process
cd /home/ubuntu/ssgAdminBE  # Replace with the actual path to your application
gunicorn -w 1 app:app  # Replace with your gunicorn command