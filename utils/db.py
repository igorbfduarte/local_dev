from contextlib import contextmanager
from dataclasses import dataclass

import psycopg2


# a data class is essencially a more robust way to build a python dictionay
@dataclass
class DBConnection:
    db: str
    user: str
    password: str
    host: str
    port: int


class WarehouseConnection:
    def __init__(self, db_conn: DBConnection):
        self.conn_url = (
            f"postgresql://{db_conn.user}:{db_conn.password}@"
            f"{db_conn.host}:{db_conn.port}/{db_conn.db}"
        )

    @contextmanager
    def managed_cursor(self, cursor_factory=None):
        self.conn = psycopg2.connect(self.conn_url)
        self.conn.autocommit = True
        self.curr = self.conn.cursor(cursor_factory=cursor_factory)
        try:
            yield self.curr
        finally:
            self.curr.close()
            self.conn.close()
