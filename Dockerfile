FROM apache/airflow:2.7.2-python3.11

USER root

# Install system dependencies
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config \
    python3-dev && \
    apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch to the airflow user
USER airflow

# Set the working directory
WORKDIR /opt/airflow

# Install Poetry
RUN pip install --no-cache-dir 'poetry==1.6.1'

# Copy project files and install project dependencies
COPY poetry.lock poetry.toml pyproject.toml ./
RUN poetry install --no-interaction
