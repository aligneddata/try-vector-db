import unittest
import os
import traceback
from abc import ABC, abstractmethod
import psycopg
from psycopg.sql import SQL, Identifier
import AppSettings
import Tools
import random
from SplitterIntf import SplitterIntf
from EmbeddingsIntf import EmbeddingsIntf
from VectorDbIntf import VectorDbIntf

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', encoding='utf-8', 
                    level=os.getenv('DEBUG_LEVEL', 'DEBUG'))


class VectorDbPgvector(VectorDbIntf):
    def __init__(self, chunk_size: int, dimension: int, splitter: SplitterIntf, embedder: EmbeddingsIntf):
        super().__init__(chunk_size, dimension, splitter, embedder)
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
            "chapter_id": "BIGINT NULL",
            "paragraph_id": "INT NULL",
            "content": "TEXT NOT NULL",
            "embedding": "vector(%d)" % dimension,
        }
        create_table(self.conn, index_name, columns)

    def load_from_file(self, index_name: str, text_file_path: str):
        with open(text_file_path, 'r') as f:
            texts = f.read()
        list_of_texts = self.splitter.split(texts, self.CHUNK_SIZE, overlap=32)
        self.load_from_texts(index_name, list_of_texts)
    
    def load_from_texts(self, index_name: str, list_of_texts):
        hasher = Tools.hashlib
        count_of_commited = 0
        with self.conn.cursor() as cur:
            for text in list_of_texts:
                text_in_chunks = self.splitter.split(text, self.CHUNK_SIZE, overlap=32)
                for chunk in text_in_chunks:
                    digest = Tools.hash_string(chunk)  # use digest to check existance first
                    with self.conn.cursor() as cur_pre_verify:
                        verify_sql = SQL("SELECT * FROM {} WHERE digest = {}").format(
                            Identifier(index_name),
                            digest
                        )
                        cur_pre_verify.execute(verify_sql)
                        if len(cur_pre_verify.fetchall()) <= 0:
                            # emb a chunk only when it is new
                            embd_str = self._get_str_from_embds(self.embedder.encode(chunk))
                            insert_sql = SQL("insert into {} (digest, embedding, content) values ({}, {}, {})").format(
                                Identifier(index_name),
                                digest,
                                embd_str,
                                chunk)
                            logging.debug(insert_sql)
                            try:
                                cur.execute(insert_sql)
                                self.conn.commit()  # Important: Commit the transaction
                                count_of_commited += 1
                                logging.info("Total commited chunks: %d" % count_of_commited)
                            except psycopg.errors.UniqueViolation as e:
                                # (traceback.format_exc())
                                error_msg = str(e)
                                logging.warning("Warning but ignore: %s" % error_msg)
                        else:
                            logging.info("Ignore: record with digest [%s] already exists" % digest)
        
    def similarity_search(self, index_name: str, query: str, k=4):
        query_embed = self._get_str_from_embds(self.embedder.encode(query))
        
        # SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;
        list_of_contexts = []
        with self.conn.cursor(row_factory=psycopg.rows.dict_row) as cur_search:
            search_sql = SQL("SELECT * FROM {} ORDER BY embedding <=> {} LIMIT {}").format(
                Identifier(index_name),
                query_embed,
                k
            )
            cur_search.execute(search_sql)
            
            for record in cur_search:
                logging.debug("Fetched result: [%d] [%s]" % (record['id'], 
                                                             record['content']))  
                list_of_contexts.append(record['content'])
        return list_of_contexts

    def _get_str_from_embds(self, embeddings):
        embd_str = '['
        for f in embeddings:
            embd_str += str(f)
            embd_str += ','
        if embd_str[-1] == ',':
            embd_str = embd_str[0:-1]
        embd_str += ']'
        return embd_str

    def close(self):
        self.conn.close()

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
            logging.info(f"Table '{table_name}' created successfully (or exists already).")

    except psycopg.Error as e:
        conn.rollback()  # Rollback in case of error
        logging.error(f"Error creating table: {e}")
    

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
                logging.info(record)

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
