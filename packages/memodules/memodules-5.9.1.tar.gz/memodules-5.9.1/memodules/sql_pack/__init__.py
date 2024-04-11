"""
SQL databases controler
"""
from typing import Any, Callable
from sqlalchemy import BinaryExpression, Column, ColumnElement, create_engine, MetaData, Table, Engine as _Engine
from sqlalchemy.orm import sessionmaker, Session as _Session, DeclarativeMeta


def items(url_or_engine: str | _Engine = 'sqlite:///:memory:', *, print_to_console=True, **kw):
    # データベースエンジンの設定
    engine = ...
    if isinstance(url_or_engine, str):
        engine = create_engine(url_or_engine, **kw)
    elif isinstance(url_or_engine, _Engine):
        engine = url_or_engine
    else:
        return {}
    Session = sessionmaker(bind=engine)
    session = Session()

    # メタデータの読み込み
    metadata = MetaData()
    metadata.reflect(bind=engine)
    result = {}
    for table_name in metadata.tables:
        result[table_name] = []
        table = Table(table_name, metadata, autoload_with=engine)
        if print_to_console: print(f"--- {table_name} ---")
        # 各テーブルからすべてのデータを取得して表示
        for row in session.query(table).all():
            result[table_name].append(row)
            if print_to_console: print(row)
    return result


def query_gen(session: _Session, table: DeclarativeMeta | None = None,
              *filters: ColumnElement[bool] | BinaryExpression[bool]):
    for item in session.query(table).filter(*filters).all():
        yield item
