# Base image for Python 3
FROM python:3

# Create the application directory
RUN mkdir -p opt/src/user

# Set the working directory for subsequent commands
WORKDIR /opt/src/user/

# Copy configuration and application files into the container
COPY configuration.py ./configuration.py
COPY user_models.py ./user_models.py
COPY app.py ./app.py
COPY requirements.txt ./requirements.txt

# Install the required Python packages
RUN pip install -r ./requirements.txt

# Set the entry point to run the application
ENTRYPOINT ["python", "./app.py"]
