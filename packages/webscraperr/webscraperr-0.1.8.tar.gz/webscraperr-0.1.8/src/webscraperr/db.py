import sqlite3
from mysql.connector import connect
from enum import IntEnum, StrEnum
from .exceptions import DatabaseNotSupportedException

class ItemsFilterByInfo(IntEnum):
    ALL = 0
    WITH_INFO = 1
    WITHOUT_INFO = 2

class DBTypes(StrEnum):
    SQLITE = 'SQLITE',
    MYSQL = 'MYSQL'

def get_items_by_filter(conn, items_filter: ItemsFilterByInfo):
    items = []
    match items_filter:
        case ItemsFilterByInfo.WITHOUT_INFO:
            items = conn.get_all_without_info()
        case ItemsFilterByInfo.WITH_INFO:
            items = conn.get_all_with_info()
        case ItemsFilterByInfo.ALL:
            items = conn.get_all()
        case _:
            raise ValueError("Invalid UpdateInfoItemsFilter value")
    return items

def get_db_class_by_config(database_config: dict):
    if database_config['TYPE'] == DBTypes.MYSQL:
        return WebScraperDBMySQL
    elif database_config['TYPE'] == DBTypes.SQLITE:
        return WebScraperDBSqlite
    else:
        raise DatabaseNotSupportedException()

def init_mysql(database_config: dict):
    temp_auth = database_config['AUTH'].copy()
    if 'database' in temp_auth:
        del temp_auth['database']
    with connect(**temp_auth) as conn:
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_config['DATABASE']}")

    with connect(**database_config['AUTH']) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS`{database_config['DATABASE']}`.`{database_config['TABLE']}` (
            `ID` INT NOT NULL AUTO_INCREMENT,
            `URL` VARCHAR(255) NOT NULL,
            `INFO` JSON NULL,
            `CATEGORY` VARCHAR(255) NULL,
            PRIMARY KEY (`ID`),
            UNIQUE INDEX `URL_UNIQUE` (`URL` ASC) VISIBLE);
        """)

def init_sqlite(database_config: dict):
    with sqlite3.connect(database_config['DATABASE']) as conn:
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {database_config['TABLE']} (
        ID   INTEGER NOT NULL
                    PRIMARY KEY AUTOINCREMENT,
        URL  TEXT    NOT NULL
                    UNIQUE,
        CATEGORY TEXT NULL,
        INFO TEXT
        );
    """)

class WebScraperDBSqlite:
    def __init__(self, config):
        self.config = config
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.config['DATABASE'])
        self.cursor = self.conn.cursor()
        self.cursor.row_factory = sqlite3.Row
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def get_all(self, category=None):
        category = 'NULL' if category is None else category
        self.cursor.execute(f"SELECT * FROM {self.config['TABLE']} WHERE CATEGORY=?", [category])
        return self.cursor.fetchall()

    def get_all_without_info(self, category=None):
        category = 'NULL' if category is None else category
        self.cursor.execute(f"SELECT * FROM {self.config['TABLE']} WHERE INFO IS NULL AND CATEGORY=?", [category])
        return self.cursor.fetchall()
    
    def get_all_with_info(self, category=None):
        category = 'NULL' if category is None else category
        self.cursor.execute(f"SELECT * FROM {self.config['TABLE']} WHERE INFO IS NOT NULL AND CATEGORY=?", [category])
        return self.cursor.fetchall()
    
    def get_by_id(self, id: int):
        self.cursor.execute(f"SELECT * FROM {self.config['TABLE']} WHERE ID=?", [id])
        return self.cursor.fetchone()

    def get_by_url(self, url: int):
        self.cursor.execute(f"SELECT * FROM {self.config['TABLE']} WHERE URL=?", [url])
        return self.cursor.fetchone()

    def save_url(self, url: str, category=None):
        category = 'NULL' if category is None else category
        self.cursor.execute(f"INSERT OR IGNORE INTO {self.config['TABLE']}(URL, CATEGORY) VALUES(?, ?)", [url, category])

    def save_urls(self, urls: list):
        self.cursor.executemany(f"INSERT OR IGNORE INTO {self.config['TABLE']}(URL, CATEGORY) VALUES(?, ?)", urls)

    def save_url_and_info(self, url: str, info: str, category=None):
        category = 'NULL' if category is None else category
        self.cursor.execute(f"INSERT OR IGNORE INTO {self.config['TABLE']}(URL, INFO) VALUES(?, ?, ?)", [url, info, category])

    def save_url_and_info_many(self, datas: list):
        self.cursor.executemany(f"INSERT OR IGNORE INTO {self.config['TABLE']}(URL, INFO, CATEGORY) VALUES(?, ?, ?)", datas)

    def set_info_by_id(self, id: int, info: str):
        self.cursor.execute(f"UPDATE {self.config['TABLE']} SET INFO=? WHERE ID=?", [info, id])
    
    def set_info_by_url(self, url: str, info: str):
        self.cursor.execute(f"UPDATE {self.config['TABLE']} SET INFO=? WHERE URL=?", [info, url])

    def clear_database(self):
        self.cursor.execute(f"DELETE FROM {self.config['TABLE']}")

class WebScraperDBMySQL:
    def __init__(self, config: dict):
        self.config = config
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = connect(**self.config['AUTH'])
        self.cursor = self.conn.cursor(dictionary=True)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()
    
    def get_all(self, category=None):
        category = 'NULL' if category is None else category
        self.cursor.execute(f"SELECT * FROM {self.config['TABLE']} WHERE CATEGORY=%s", (category, ))
        return self.cursor.fetchall()
    
    def get_all_without_info(self, category=None):
        category = 'NULL' if category is None else category
        self.cursor.execute(f"SELECT * FROM {self.config['TABLE']} WHERE INFO IS NULL AND CATEGORY=%s", (category, ))
        return self.cursor.fetchall()
    
    def get_all_with_info(self, category=None):
        category = 'NULL' if category is None else category
        self.cursor.execute(f"SELECT * FROM {self.config['TABLE']} WHERE INFO IS NOT NULL AND CATEGORY=%s", (category, ))
        return self.cursor.fetchall()
    
    def get_by_url(self, url: str):
        self.cursor.execute(f"SELECT * FROM {self.config['TABLE']} WHERE URL=%s", (url, ))
        return self.cursor.fetchone()

    def get_by_id(self, id: int):
        self.cursor.execute(f"SELECT * FROM {self.config['TABLE']} WHERE ID=%s", (id, ))
        return self.cursor.fetchone()

    def save_url(self, url: str, category=None):
        category = 'NULL' if category is None else category
        self.cursor.execute(f"INSERT IGNORE INTO {self.config['TABLE']}(URL, CATEGORY) VALUES(%s, %s)", (url, category))
    
    def save_urls(self, urls: str):
        self.cursor.executemany(f"INSERT IGNORE INTO {self.config['TABLE']}(URL, CATEGORY) VALUES(%s, %s)", urls)
    
    def save_url_and_info(self, url: str, info: str, category=None):
        category = 'NULL' if category is None else category
        self.cursor.execute(f"INSERT IGNORE INTO {self.config['TABLE']}(URL, INFO, CATEGORY) VALUES(%s, %s, %s)", (url, info, category))

    def save_url_and_info_many(self, datas: list):
        self.cursor.executemany(f"INSERT IGNORE INTO {self.config['TABLE']}(URL, INFO, CATEGORY) VALUES(%s, %s, %s)", datas)

    def set_info_by_id(self, id: int, info: str):
        self.cursor.execute(f"UPDATE {self.config['TABLE']} SET INFO=%s WHERE ID=%s", (info, id))

    def set_info_by_url(self, url: str, info: str):
        self.cursor.execute(f"UPDATE {self.config['TABLE']} SET INFO=%s WHERE URL=%s", (info, url))
    
    def clear_database(self):
        self.cursor.execute(f"DELETE FROM {self.config['TABLE']}")