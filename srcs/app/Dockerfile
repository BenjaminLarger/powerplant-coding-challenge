# Use a lightweight Python image
FROM python:3.8-slim

RUN mkdir -p /build

# Copy the requirements file into the container
COPY ./tools/requirements.txt ./build/requirements.txt

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r ./build/requirements.txt

# Copy the main application code into the container
COPY ./tools/main.py ./build/main.py

# Expose port 8888 to match the Flask app's port
EXPOSE 8888

# Set environment variables
ENV FLASK_APP=./build/main.py  

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=8888"]
