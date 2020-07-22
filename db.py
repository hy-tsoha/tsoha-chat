import psycopg2 as pg
import operator
import os
from psycopg2.extras import NamedTupleCursor


class Session:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def open(self):
        self.connection = pg.connect(**self.kwargs)
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def __enter__(self):
        self.open()
        return self.cursor

    def __exit__(self, exception, value, traceback):
        if not exception:
            self.connection.commit()
        self.close()


class DatabaseManager:
    def __init__(self, **kwargs):
        self.database = kwargs.get("database", None)
        self.host = kwargs.get("host", None)
        self.port = kwargs.get("port", None)
        self.user = kwargs.get("user", None)
        self.password = kwargs.get("password", None)
        self.factory = kwargs.get("factory", NamedTupleCursor)

    def get_params(self):
        params = (
            ("dbname", self.database),
            ("host", self.host),
            ("port", self.port),
            ("user", self.user),
            ("password", self.password),
        )
        return dict(filter(operator.itemgetter(1), params))

    def get_dsn(self):
        return " ".join(map("=".join, self.params.items()))

    def get_session(self):
        return Session(**self.params, cursor_factory=self.factory)

    params = property(get_params)
    dsn = property(get_dsn)
    session = property(get_session)


db = DatabaseManager(database=os.getenv("POSTGRES_DATABASE"))
