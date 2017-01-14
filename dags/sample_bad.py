"""File that raises an exception on import."""

import datetime as dt

import airflow.models as af_models
from airflow.operators import bash_operator as bash_op

DAG = af_models.DAG(
    dag_id='sample_good',
    start_date=dt.datetime(2017, 1, 11),
)

task1 = bash_op.BashOperator(
    task_id='task1',
    bash_command='echo "Hello"',
    dag=DAG,
)

raise Exception('oops')
