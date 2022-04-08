import sqlite3
import logging

log = logging.getLogger(__name__)


class WAD():
    def __init__(self, id):
        self.id = id
        self.filenames = None
        self.size = None
        self.md5 = None
        self.sha1 = None
        self.sha256 = None
        self.wad_type = None
        self.iwad = None
        self.engines = None
        self.lumps = None
        self.downloaded = 0
        # maps maybe?


class Database():
    __DB_Location = "./wad-archive.db"

    def __init__(self):
        self.__connection = sqlite3.connect(
            self.__DB_Location,
            check_same_thread=False
        )
        self.cursor = self.__connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS wad (
                id TEXT PRIMARY_KEY UNIQUE,
                filenames TEXT,
                size TEXT,
                md5 TEXT,
                sha1 TEXT,
                sha256 TEXT,
                wad_type TEXT,
                iwad TEXT,
                engines TEXT,
                lumps TEXT,
                downloaded INTEGER default 0
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS download_url (
                id INTEGER PRIMARY KEY ASC,
                url TEXT,
                wad_id INTEGER,
                FOREIGN KEY (wad_id) REFERENCES wad(id)
        )""")

    def insert_wad(self, wad):
        sql = """
            INSERT INTO wad (
                id, filenames, size, md5, sha1, sha256, wad_type,
                iwad, engines, lumps, downloaded
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )"""
        try:
            self.cursor.execute(sql, (wad.id, wad.filenames, wad.size, wad.md5,
                                      wad.sha1, wad.sha256, wad.wad_type,
                                      wad.iwad, wad.engines, wad.lumps,
                                      wad.downloaded))
            self.__connection.commit()
        except sqlite3.IntegrityError:
            log.debug(f"WAD {wad.id} already exists in database")
        return self.cursor.lastrowid

    def insert_download_url(self, wad, url):
        sql = """
            INSERT INTO download_url (
                url, wad_id
            ) VALUES (
                ?, ?
            )"""
        self.cursor.execute(sql, (url, wad.id))
        self.__connection.commit()

    def replace_wad(self, wad):
        sql = """
            INSERT OR REPLACE INTO wad (
                id, filenames, size, md5, sha1, sha256, wad_type,
                iwad, engines, lumps, downloaded
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )"""
        try:
            self.cursor.execute(sql, (wad.id, wad.filenames, wad.size, wad.md5,
                                      wad.sha1, wad.sha256, wad.wad_type,
                                      wad.iwad, wad.engines, wad.lumps,
                                      wad.downloaded))
            self.__connection.commit()
        except sqlite3.IntegrityError:
            log.debug(f"WAD {wad.id} already exists in database")
        return self.cursor.lastrowid

    def set_wad_downloaded(self, wad):
        sql = """
            UPDATE wad
            SET downloaded = 1
            WHERE id = ?
        """
        self.cursor.execute(sql, (wad.id, ))
        self.__connection.commit()

    def get_wad(self, id):
        sql = """
            SELECT * FROM wad
            WHERE id = ?
        """
        self.cursor.execute(sql, (id, ))
        return self.cursor.fetchone()

    def get_not_downloaded_wads(self):
        sql = """
            SELECT * FROM wad
            WHERE downloaded = 0
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_wad_url(self, wad):
        sql = """
            SELECT * FROM download_url
            WHERE wad_id = ?
        """
        self.cursor.execute(sql, (wad.id, ))
        return self.cursor.fetchall()

    def close(self):
        self.__connection.close()

    def __del__(self):
        self.__connection.close()
