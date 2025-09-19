# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Run the app. We use the 'gevent' worker class for WebSocket support.
# This is the corrected command.
CMD ["gunicorn", "--worker-class", "gevent", "-w", "1", "main:app", "-b", "0.0.0.0:5000"]

