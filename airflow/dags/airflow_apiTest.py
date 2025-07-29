import logging
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
from airflow.hooks.base import BaseHook
from datetime import timezone

# KST 시간대 정의 (UTC+9)
KST = timezone(timedelta(hours=9))

def call_api():
    """API를 호출하고 응답을 로깅합니다."""
    try:
        # Airflow Connection에서 API URL 가져오기
        #conn = BaseHook.get_connection("api_test-conn")
        #api_url = conn.host
        #response = requests.get(api_url, timeout=10)
        response = requests.get("http://172.20.100.95:33333/apitest")
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        logging.info(f"API Response: {response.status_code} - {response.text[:100]}")
        return response.status_code
    except requests.Timeout:
        logging.error("API request timed out.")
        raise
    except requests.HTTPError as e:
        logging.error(f"API call failed with HTTP error: {e}")
        raise
    except requests.RequestException as e:
        logging.error(f"API call failed: {e}")
        raise

def conditional_call_api(**context):
    execution_time = context['execution_date'].astimezone(KST)
    scheduled_time = execution_time.replace(minute=0, second=10, microsecond=0)
    current_time_kst = datetime.now(KST)
    run_id = context['run_id']

    start_date_kst = context['dag'].default_args['start_date'].astimezone(KST)
    if execution_time == start_date_kst: 
        logging.info(f"First run (run_id: {run_id}); calling API immediately.")
        call_api()
        return
    
    if current_time_kst >= scheduled_time:
        logging.info(f"Scheduled time reached (run_id: {run_id}); calling API at {current_time_kst}.")
        call_api()
    else:
        logging.info(f"Not yet scheduled time (run_id: {run_id}); current time is {current_time_kst}, scheduled time is {scheduled_time}. Skipping API call.")  

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 7, 29, 15, 0, 10, tzinfo=KST),  # KST 시간대 설정
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'api_test_dag',
    default_args=default_args,
    schedule_interval='@hourly',  # 매시간 실행
    catchup=False,  # 이전 실행 건은 무시
    description='Call external API every hour at 10s mark(KST), run immediately on first run',
) as dag:
    api_task = PythonOperator(
        task_id='call_api_task',
        python_callable=conditional_call_api,
        provide_context=True,
    )
