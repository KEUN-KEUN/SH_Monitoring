import logging
from datetime import datetime

from airflow import DAG

from airflow.operators.python import PythonOperator
import requests
from datetime import timedelta


def call_api():
    response = requests.get("http://172.20.100.95:33333/apitest")
    logging.info(f"API Response: {response.status_code} - {response.text}")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 7, 21),
}

dag = DAG(
    'api_test_dag',
    default_args=default_args,
    schedule_interval=timedelta(seconds=30),  # Every 30 seconds
    catchup=False,  # Do not run missed intervals
)

api_task = PythonOperator(
    task_id='call_api_task',
    python_callable=call_api,
    dag=dag,
)

"현재 2025.7.28이다. start_date의 값은 무엇을 의미합니까?"