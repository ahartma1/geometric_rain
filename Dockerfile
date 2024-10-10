# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the PYTHONPATH environment variable to include the src directory
ENV PYTHONPATH=/app/src

# Run the game using pybag
CMD ["pybag", "src/game.py"]