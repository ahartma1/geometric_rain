# Step 1: Use an ARM-compatible base image with Python
FROM python:3.10-slim-bullseye

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Copy your Pygame project into the Docker container
COPY . .

# Step 4: Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libasound2-dev \
    libjpeg-dev \
    zlib1g-dev \
    ffmpeg \
    mime-support \
    && pip install --upgrade pip

# Step 5: Install Pygbag and Pygame
RUN pip install pygbag pygame numpy appdirs

# Step 6: Run Pygbag to build the app for WebAssembly
RUN pygbag src/geometric_rain/  # Adjust path as per your project structure

# Step 7: Install a lightweight HTTP server to serve the WebAssembly files
RUN apt-get install -y python3-pip && pip3 install httpserver

# Step 8: Expose the port where the web app will be served
EXPOSE 8000

# Step 9: Command to run the server and serve the app in the browser
CMD ["python3", "-m", "http.server", "8000"]
