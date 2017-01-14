"""File that contains no DAGs."""

from airflow.operators import bash_operator as bash_op

task1 = bash_op.BashOperator(
    task_id='task1',
    bash_command='echo "Hello"',
)
