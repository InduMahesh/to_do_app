# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY app.py .

# Expose the application port
EXPOSE 3000

# Run the application
CMD ["python", "app.py"]
