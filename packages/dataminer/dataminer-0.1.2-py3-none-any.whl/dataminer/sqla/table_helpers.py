from dataclasses import dataclass
from typing import Optional

from sqlalchemy import Engine, MetaData, Table


@dataclass
class MetaColumn:
    name: str
    type: str
    length: Optional[int] = None
    comment: Optional[str] = None


class TableHelper:
    def __init__(self, engine: Engine, table: str, schema: str = None):
        self.engine = engine
        self.meta = MetaData(schema=schema) if schema else MetaData()
        self.table = Table(table, self.meta, autoload_with=self.engine)

    def get_columns(self) -> list[MetaColumn]:
        result = []
        for column in self.table.columns:
            if hasattr(column.type, "length"):
                result.append(
                    MetaColumn(name=column.name,
                               type=column.type.python_type.__name__,
                               length=column.type.length,
                               comment=column.comment
                               )
                )
            else:
                result.append(
                    MetaColumn(name=column.name,
                               type=column.type.python_type.__name__,
                               comment=column.comment
                               )
                )
        return result

    def batch_insert(self, data: list[dict]):
        with self.engine.connect() as conn:
            with conn.begin():
                conn.execute(self.table.insert(), data)
