FROM python:3.12-alpine

# Set the wokr dir of course
WORKDIR /app

# Copy all files to ma container
COPY . .

