from typing import Any

import ydb
from ydb.convert import ResultSets

import config

if config.USE_YDB:
    driver = ydb.Driver(
        endpoint=config.YDB_ENDPOINT,
        database=config.YDB_DATABASE,
        credentials=ydb.credentials_from_env_variables(),
    )

    driver.wait(timeout=5)

    session = driver.table_client.session().create()


def execute_query(query: str, query_args: dict[str, Any]) -> ResultSets:
    prepared_query = session.prepare(query)
    prepared_query_args = _prepare_query_args(query_args)
    return session.transaction().execute(prepared_query, prepared_query_args, commit_tx=True)


def _prepare_query_args(args: dict[str, str]) -> dict[str, bytes]:
    return {key: value.encode('utf-8') for key, value in args.items()}
