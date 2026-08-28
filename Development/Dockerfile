# Use the official Python image from the Docker Hub
FROM python:3.11.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables (if any)
ENV FLASK_ENV=production

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "BE_SERVER.py"]
