import unittest
from abc import ABC, abstractmethod
import psycopg
from psycopg.sql import SQL, Identifier
from AppSettings import DATABASES
import Tools
import random


class VectorDbPgvector(ABC):
    def __init__(self):
        super().__init__()
        # postgresql://[userspec@][hostspec][/dbname][?paramspec]
        connection_info = "postgresql://%s:%s@%s:%s/%s" % (
            DATABASES['default']['USER'],
            DATABASES['default']['PASSWORD'],
            DATABASES['default']['HOST'],
            DATABASES['default']['PORT'],
            DATABASES['default']['NAME'],
        )
        self.conn = psycopg.connect(conninfo=connection_info)
        
    # CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));
    def create_or_get_index(self, index_name: str, dimension: int):
        columns = {
            "id": "bigserial PRIMARY KEY",
            "digest": "VARCHAR(255) NOT NULL UNIQUE",
            "created_at": "TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP",
            "embedding": "vector(%d)" % dimension,
        }
        create_table(self.conn, index_name, columns)

    def load_from_file(self, index_name: str, filename: str):
        pass
    
    def load_from_texts(self, index_name: str, list_of_texts):
        pass
    
    def similarity_search(self, query: str, k=4):
        pass


def create_table(conn, table_name, columns):
    """Creates a table in the PostgreSQL database.
    Args:
        conn: The psycopg connection object.
        table_name: The name of the table to create (string).
        columns: A dictionary where keys are column names (strings) and
            values are column definitions (strings, e.g., "INT PRIMARY KEY",
            "VARCHAR(255) NOT NULL").
    """
    try:
        with conn.cursor() as cur:
            # Use psycopg.sql.SQL and psycopg.sql.Identifier to prevent SQL injection
            table_identifier = Identifier(table_name)

            column_definitions = []
            for col_name, col_type in columns.items():
                column_identifier = Identifier(col_name)
                column_definitions.append(SQL("{} {}").format(column_identifier, SQL(col_type)))

            # Construct the CREATE TABLE statement
            create_table_sql = SQL("CREATE TABLE {} ({})").format(
                table_identifier, SQL(", ").join(column_definitions)
            )

            cur.execute(create_table_sql)
            conn.commit()  # Important: Commit the transaction
            print(f"Table '{table_name}' created successfully.")

    except psycopg.Error as e:
        conn.rollback()  # Rollback in case of error
        print(f"Error creating table: {e}")
    

class TestVectorDbPgvector(unittest.TestCase):
    def setUp(self):
        self.vdb = VectorDbPgvector()

    def tearDown(self):
        if self.vdb.conn != None:
            self.vdb.conn.close()
    
    def test_1_conn(self):
        with self.vdb.conn.cursor() as cur:
            cur.execute("SELECT * FROM test")
            # cur.fetchall() fetchone() fetchmany()
            for record in cur:
                print(record)

    def test_2_create_index(self):
        self.vdb.create_or_get_index("myindex_" + str(random.randint(0,999999)), 64)

