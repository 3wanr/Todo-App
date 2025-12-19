"""Database utilities for the Todo-App server.

This module provides small helpers to connect to a Postgres database and
to execute simple queries. By default it reads configuration from
`config/db.yml` located at the project root (two directories above
`server/api`).

Notes:
- Integration code that requires a live database should guard calls to
    these helpers (tests use mocking or an env var to enable integration runs).
- The config file format is a YAML mapping with keys: `database`,
    `user`, `password`, `host`, `port`.
"""

import psycopg2
import yaml
import os

def connect():
    """Create and return a new psycopg2 connection.

    Reads DB connection parameters from `config/db.yml` located at the
    project root (two directories above this file). The YAML must contain
    the keys: `database`, `user`, `password`, `host`, `port`.

    Returns:
        psycopg2.extensions.connection: a new database connection.

    Raises:
        FileNotFoundError: if the config file doesn't exist.
        KeyError: if required config keys are missing.
        psycopg2.OperationalError: for connection-related errors.
    """
    config = {}
    # config directory is at project root: ../../config/db.yml from server/api
    yml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'db.yml'))

    with open(yml_path, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    return psycopg2.connect(
        dbname=config['database'],
        user=config['user'],
        password=config['password'],
        host=config['host'],
        port=config['port']
    )

def exec_get_one(sql, args=None):
    """Execute a query and return a single row.

    Args:
        sql (str): SQL query string. Use placeholders for parameters
            (psycopg2 style, e.g. %s).
        args (tuple|list|dict, optional): Parameters for the query.

    Returns:
        tuple|None: The first row returned by the query, or ``None`` if
            no rows were found.

    Notes:
        This helper opens a new connection per call and closes it when
        finished. For higher performance use a connection pool.
    """
    if args is None:
        args = ()
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, args)
    one = cur.fetchone()
    conn.close()
    return one

def exec_commit(sql, args=None):
    """Execute a modifying statement and commit the transaction.

    Args:
        sql (str): SQL statement (INSERT/UPDATE/DELETE/etc.).
        args (tuple|list|dict, optional): Parameters for the statement.

    Returns:
        Any: The return value of ``cursor.execute`` (usually None). If you
        need affected row counts use ``cursor.rowcount`` inside a custom
        wrapper.

    Notes:
        This function opens a connection, executes the statement, commits,
        and closes the connection. It is intended for simple scripts and
        tests; use a transaction manager or ORM for production code.
    """
    if args is None:
        args = ()
    conn = connect()
    cur = conn.cursor()
    result = cur.execute(sql, args)
    conn.commit()
    conn.close()
    return result

def exec_sql_file(file_path, stop_on_error=True):
    """Execute SQL statements loaded from a file.

    The file is read and split on semicolons; each non-empty statement is
    executed in sequence. This is a lightweight helper intended for
    simple schema or seed scripts used in development and tests.

    Limitations:
    - Splitting on semicolons is naive and may fail for complex SQL
      that includes procedure/function bodies containing semicolons.
    - For robust script execution consider using a SQL-aware runner or
      psql/psycopg2's advanced facilities.

    Args:
        file_path (str): Path to the SQL file to execute.
        stop_on_error (bool): If True (default) the function will roll
            back and raise on the first error. If False it will attempt
            to continue executing subsequent statements and will commit
            any successful statements.

    Returns:
        int: Number of statements successfully executed.

    Raises:
        FileNotFoundError: if the `file_path` does not exist.
        Exception: re-raises the underlying DB exception when
            `stop_on_error` is True.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Naive split on semicolon. Keep simple for typical schema/seed files.
    statements = [s.strip() for s in content.split(';')]

    conn = connect()
    cur = conn.cursor()
    executed = 0

    try:
        for stmt in statements:
            if not stmt:
                continue
            try:
                cur.execute(stmt)
                executed += 1
            except Exception:
                conn.rollback()
                if stop_on_error:
                    conn.close()
                    raise
                # else: swallow and continue to next statement
        conn.commit()
    finally:
        conn.close()

    return executed