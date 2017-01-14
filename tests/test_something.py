"""Tests for afexample.something."""

import sqlalchemy as sa

from afexample import something


def test_do_something(tconn):
    assert not tconn.engine.dialect.has_table(tconn, 'test')
    something.do_something(tconn)
    result = tconn.execute('SELECT * FROM test')
    rows = [dict(r) for r in result]
    rows.sort(key=lambda r: tuple(sorted(r.items())))
    assert rows == [
        {'id': 1, 'value': 'hello'},
        {'id': 2, 'value': 'there'}
    ]


def test_do_something_task(pg_dburi, test_conn_id, request):
    engine = sa.create_engine(pg_dburi)
    request.addfinalizer(engine.dispose)
    with engine.begin() as conn:
        assert not conn.engine.dialect.has_table(conn, 'test')

    something.do_something_task(test_conn_id)

    with engine.begin() as conn:
        result = conn.execute('SELECT * FROM test')
        rows = [dict(r) for r in result]
    rows.sort(key=lambda r: tuple(sorted(r.items())))
    assert rows == [
        {'id': 1, 'value': 'hello'},
        {'id': 2, 'value': 'there'}
    ]
