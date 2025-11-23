from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def print_hello():
    return 'Hello form Dockerized Airflow!'


with DAG('docker_test_dag', start_date=datetime(2023, 1, 1), schedule_interval=None) as dag:
    task1 = PythonOperator(
        task_id='hello_task',
        python_callable=print_hello
    )
