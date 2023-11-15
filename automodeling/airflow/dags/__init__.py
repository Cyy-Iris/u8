"""`dags` package contains all the airflow dags definition.

DAG are defined as python module. One module per DAG. This repository leverage task flow
with a custom decorator to help share file dependencies between tasks and seemlessly
load and upload files from the s3 storage layer.

The package contains the following DAG:
    * `mod`:main: the main DAG for automodelling starting from a PDF to a graph.
"""
