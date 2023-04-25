# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose port 5000 for the Flask app to listen on
EXPOSE 5000

# Define environment variables
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

# Run the command to start the app
CMD ["flask", "run"]
