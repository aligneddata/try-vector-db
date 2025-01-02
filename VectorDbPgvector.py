import unittest
import traceback
from abc import ABC, abstractmethod
import psycopg
from psycopg.sql import SQL, Identifier
import AppSettings
import Tools
import random
from SplitterSimple import SplitterSimple
from EmbeddingsSimple import EmbeddingsSimple


class VectorDbPgvector(ABC):
    def __init__(self):
        super().__init__()
        # postgresql://[userspec@][hostspec][/dbname][?paramspec]
        connection_info = "postgresql://%s:%s@%s:%s/%s" % (
            AppSettings.DATABASES['default']['USER'],
            AppSettings.DATABASES['default']['PASSWORD'],
            AppSettings.DATABASES['default']['HOST'],
            AppSettings.DATABASES['default']['PORT'],
            AppSettings.DATABASES['default']['NAME'],
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

    def load_from_file(self, index_name: str, text_file_path: str):
        with open(text_file_path, 'r') as f:
            texts = f.read()
        splitter = SplitterSimple()
        list_of_texts = splitter.split(texts, AppSettings.SPLITTER_CHUNK_SIZE, overlap=0)
        self.load_from_texts(index_name, list_of_texts)
    
    def load_from_texts(self, index_name: str, list_of_texts):
        splitter = SplitterSimple()
        embd = EmbeddingsSimple()
        hasher = Tools.hashlib
        count_of_commited = 0
        with self.conn.cursor() as cur:
            for text in list_of_texts:
                text_in_chunks = splitter.split(text, AppSettings.SPLITTER_CHUNK_SIZE)
                for chunk in text_in_chunks:
                    print(chunk)
                    embeddings = embd.encode(chunk, AppSettings.EMBEDDINGS_DIM)
                    print(embeddings)
                    # INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]');
                    # insert into myindex (digest, embedding) values ('12345678', '[1,2,3,4]');
                    embd_str = self._get_str_from_embds(embeddings)
                    print(embd_str)
                    digest = Tools.hash_string(chunk)
                    with self.conn.cursor() as cur_pre_verify:
                        verify_sql = SQL("SELECT * FROM {} WHERE digest = {}").format(
                            Identifier(index_name),
                            digest
                        )
                        cur_pre_verify.execute(verify_sql)
                        if len(cur_pre_verify.fetchall()) <= 0:
                            insert_sql = SQL("insert into {} (digest, embedding) values ({}, {})").format(
                                Identifier(index_name),
                                digest,
                                embd_str)
                            print(insert_sql)
                            try:
                                cur.execute(insert_sql)
                                self.conn.commit()  # Important: Commit the transaction
                                count_of_commited += 1
                                print("Total commited chunks: %d" % count_of_commited)
                            except psycopg.errors.UniqueViolation as e:
                                # print(traceback.format_exc())
                                error_msg = str(e)
                                print("Warning but ignore: %s" % error_msg)
                        else:
                            print("Ignore: record with digest [%s] already exists" % digest)
        
    def similarity_search(self, query: str, k=4):
        pass

    def _get_str_from_embds(self, embeddings):
        embd_str = '['
        for f in embeddings:
            embd_str += str(f)
            embd_str += ','
        if embd_str[-1] == ',':
            embd_str = embd_str[0:-1]
        embd_str += ']'
        return embd_str


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
            create_table_sql = SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
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
        self.index_name = 'myindex'

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
        self.vdb.create_or_get_index(self.index_name, 4)

    def test_3_load_texts(self):
        test_texts = [
            '01234567890',
            'abcdefghijk'
        ]
        self.vdb.load_from_texts(self.index_name, test_texts)

    def test_4_load_file(self):
        self.vdb.load_from_file(self.index_name, 'z1.txt')
