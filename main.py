import json
import boto3
from airflow import DAG
from airflow.contrib.operators.emr_create_job_flow_operator import EmrCreateJobFlowOperator
from datetime import datetime, timedelta


def main():
    client = boto3.client('emr',region_name='us-east-1' )
    result = json.loads(open("emr_profile.json", "r").read())
    print(result['ManagedScalingPolicy'])
    client.run_job_flow(**result)

def create_dag():
    dag = DAG(
        dag_id='test',
        default_args={'owner': 'airflow',
                      'depends_on_past': False,
                      'email': [],
                      'email_on_failure': False,
                      'email_on_retry': False,
                      'retries': 1,
                      'retry_delay': timedelta(minutes=5), },
        dagrun_timeout=timedelta(days=2),
        schedule_interval=None,
        start_date=datetime(2021, 1, 1),
        tags=['test-spot'],
    )

    cluster_creator = EmrCreateJobFlowOperator(
        task_id='create_job_flow',
        job_flow_overrides=None,
        aws_conn_id='aws_default',
        emr_conn_id='emr_profile',
        dag=dag
    )


if __name__ == '__main__':
    main()

