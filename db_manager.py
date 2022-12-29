import sqlite3, os

from db_model import DB_MODEL

def model_factory(cursor, row):
    try:
        return DB_MODEL(row[0], row[1], row[2], row[3])
    except IndexError:
        return row

class DBManager:
    def __init__(self, db_name):
        this_dir = os.path.dirname(__file__)
        self.db_path = os.path.join(this_dir, db_name)
        self.connection = self._connect_db() # one db user, one connection
        self.connection.row_factory = model_factory
        self.cursor = self.connection.cursor()
        self._create_pages_table()

    def _connect_db(self):
        # Creates a database if it doesn't exist
        return sqlite3.connect(self.db_path)

    def _create_pages_table(self):
        # This schema should reflect the db_model.py
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pages 
            ([url] TEXT PRIMARY KEY,
             [type] TEXT,
             [visited] BOOLEAN,
             [links_out] TEXT)
            """)
        self.connection.commit()
    
    '''
    def create(self, url, type, visited, links_out):
        self.cursor.execute("""
            INSERT OR IGNORE INTO pages (url, type, visited, links_out)
            VALUES (?, ?, ?, ?)""",
            [url, type, visited, links_out])
        self.connection.commit()
    '''

    def create(self, db_model):
        self.cursor.execute("""
            INSERT OR IGNORE INTO pages (url, type, visited, links_out)
            VALUES (?, ?, ?, ?)""",
            [db_model.url, db_model.type, db_model.visited, db_model.links_out])
        self.connection.commit()

    def retrieve_one_unvisited(self):
        return self.cursor.execute("""
            SELECT *
            FROM pages
            WHERE visited = 0""").fetchone()

    def retrieve(self, url):
        return self.cursor.execute("""
            SELECT *
            FROM pages
            WHERE url = ?""",
            [url]).fetchone()

    def update(self, db_model):
        self.cursor.execute("""
            UPDATE pages 
            SET type=?, visited=?, links_out=?
            WHERE url = ?""",
            [db_model.type, db_model.visited, db_model.links_out, db_model.url])
        self.connection.commit()

    def count(self):
        return self.cursor.execute("""
            SELECT COUNT(*)
            FROM pages""").fetchone()[0]
