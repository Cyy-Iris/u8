FROM apache/airflow:2.7.2-python3.11
# Install the desired Python version

WORKDIR /opt/airflow
 
COPY poetry.lock poetry.toml pyproject.toml ./
 
RUN pip install --no-cache-dir 'poetry==1.6.1' && \
    poetry install --no-interaction

#ENV PYTHONPATH = "/opt/airflow:/opt/airflow/.venv/lib/python3.11/site-packages:${PYTHONPATH}"
