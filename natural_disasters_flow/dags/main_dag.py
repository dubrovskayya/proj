import subprocess
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
PYTHON_PATH = os.getenv('PYTHON_PATH')
PROJECT_PATH = os.getenv('PROJECT_PATH')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=3)
}


# run the producer script as a subprocess
def run_producer():
    subprocess.run([PYTHON_PATH, f'{PROJECT_PATH}/producer.py'], check=True)


# run the producer script as a subprocess
def run_consumer():
    subprocess.run([PYTHON_PATH, f'{PROJECT_PATH}/consumer.py'], check=True)


with DAG(
        dag_id='natural_disaster_flow',
        default_args=default_args,
        schedule_interval=timedelta(hours=3),
        catchup=False
) as dag:
    producer_task = PythonOperator(
        task_id='run_producer',
        python_callable=run_producer
    )

    consumer_task = PythonOperator(
        task_id='run_consumer',
        python_callable=run_consumer
    )

    # the consumer is launched after the producer is finished
    producer_task >> consumer_task
