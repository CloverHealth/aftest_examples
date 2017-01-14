"""Configure the test suite."""

import os

import pytest
import sqlalchemy as sa
import testing.postgresql

TEST_AIRFLOW_HOME = os.path.join(
    os.path.dirname(__file__),
    'test_airflow_home',
)
TEST_ENV_VARS = {
    'AIRFLOW_HOME': TEST_AIRFLOW_HOME,
}


def pytest_configure(config):
    """Configure and init envvars for airflow."""
    config.old_env = {}
    for key, value in TEST_ENV_VARS.items():
        config.old_env[key] = os.getenv(key)
        os.environ[key] = value


def pytest_unconfigure(config):
    """Restore envvars to old values."""
    for key, value in config.old_env.items():
        if value is None:
            del os.environ[key]
        else:
            os.environ[key] = value


@pytest.fixture(scope='session')
def pg_dburi(request):
    """Session-wide test database."""
    test_db = testing.postgresql.Postgresql()
    request.addfinalizer(test_db.stop)
    return test_db.url()


@pytest.fixture
def tconn(pg_dburi, request):
    """Connection in a transaction that will rollback after the test."""
    engine = sa.create_engine(pg_dburi)
    request.addfinalizer(engine.dispose)
    conn = engine.connect()
    request.addfinalizer(conn.close)
    transaction = conn.begin()
    request.addfinalizer(transaction.rollback)
    return conn


@pytest.fixture
def test_conn_id(pg_dburi, request):
    """Fixture to provide postgres at the airflow conn_id 'test'."""
    def resetdb():
        """Reset the db to a clean slate."""
        engine = sa.create_engine(pg_dburi)
        with engine.begin() as conn:
            conn.execute('DROP SCHEMA public CASCADE')
            conn.execute('CREATE SCHEMA public')
    request.addfinalizer(resetdb)

    old_test_conn = os.getenv('AIRFLOW_CONN_TEST_CONN')
    def resetenv():
        """Reset environment."""
        if old_test_conn is None:
            del os.environ['AIRFLOW_CONN_TEST_CONN']
        else:
            os.environ['AIRFLOW_CONN_TEST_CONN'] = old_test_conn
    os.environ['AIRFLOW_CONN_TEST_CONN'] = pg_dburi
    request.addfinalizer(resetenv)

    return 'test_conn'
