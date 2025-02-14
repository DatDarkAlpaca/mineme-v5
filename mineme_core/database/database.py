import os
import psycopg2
from psycopg2.extensions import connection

from mineme_core.constants import *


def create_database_connection() -> connection:
    database_name = os.environ.get('DATABASE_NAME')
    host = os.environ.get('DATABASE_HOST')
    user = os.environ.get('DATABASE_USER')
    password = os.environ.get('DATABASE_PASSWORD')
    port = os.environ.get('DATABASE_PORT')

    database_connection = psycopg2.connect(database=database_name,
                            host=host,
                            user=user,
                            password=password,
                            port=port)
    database_connection.set_session(autocommit=True)

    return database_connection
