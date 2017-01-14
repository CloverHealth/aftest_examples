"""Sample library function to do a something."""

from airflow.hooks import base_hook
import sqlalchemy as sa


def get_engine(conn_id):
    """Get a sqlalchemy engine from an airflow connection id."""
    connection = base_hook.BaseHook.get_connection(conn_id)
    uri = (
        '{c.conn_type}://{c.login}:{c.password}@{c.host}:{c.port}/{c.schema}'
        .format(c=connection)
    )
    return sa.create_engine(uri)


def do_something_task(conn_id):
    """Wraper around do_something to fit into airflow.

    This method isn't properly tested because it's a pain to deal with
    Airflow connections in test.
    """
    engine = get_engine(conn_id)
    with engine.begin() as conn:
        do_something(conn)


def do_something(conn):
    """Function that actually does something, and gets proper tested."""
    table = sa.Table(
        'test', sa.MetaData(conn),
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('value', sa.Text, unique=True),
    )
    table.drop(conn, checkfirst=True)
    table.create(conn)
    conn.execute(table.insert(), [
        {'value': 'hello'},
        {'value': 'there'},
    ])
