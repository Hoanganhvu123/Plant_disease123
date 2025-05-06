# Use Miniconda base image
FROM continuumio/miniconda3:latest

# Set working directory inside the container
WORKDIR /app

# Copy requirements file first to leverage Docker cache
COPY ["Flask Deployed App/requirements.txt", "./"]

# Create conda environment with Python 3.9
RUN conda create -n plant_env python=3.9 -y

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "plant_env", "/bin/bash", "-c"]

# Install dependencies using pip inside the conda environment
# Upgrade pip first
RUN pip install --upgrade pip wheel setuptools
RUN pip install -r requirements.txt --no-cache-dir

# Copy the rest of the application code from the subfolder
COPY ["Flask Deployed App/", "./"]

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application INSIDE the conda environment
# Use the exec form of CMD and specify conda run
CMD ["conda", "run", "-n", "plant_env", "python", "app.py"] 