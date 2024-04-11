"""
SQL databases controler
"""
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker


def items(url: str = 'sqlite:///:memory:'):
    # データベースエンジンの設定
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    session = Session()

    # メタデータの読み込み
    metadata = MetaData()
    metadata.reflect(bind=engine)

    for table_name in metadata.tables:
        table = Table(table_name, metadata, autoload_with=engine)
        print(f"--- {table_name} ---")
        # 各テーブルからすべてのデータを取得して表示
        for row in session.query(table).all():
            print(row)
