"""Simple dag that uses the library code."""

import datetime as dt

import airflow.models as af_models
from airflow.operators import python_operator as py_op

from afexample import something

DAG = af_models.DAG(
    dag_id='sample_good',
    start_date=dt.datetime(2017, 1, 11),
)

task1 = py_op.PythonOperator(
    task_id='task1',
    python_callable=something.do_something_task,
    op_kwargs={
        'conn_id': 'test_conn',
    },
    dag=DAG,
)
