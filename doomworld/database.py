import sqlite3


class File():
    def __init__(self, id):
        self.id = id
        self.title = None
        self.description = None
        self.views = None
        self.downloads = None
        self.submitted = None
        self.author = None
        self.credits = None
        self.base = None
        self.build_time = None
        self.editors_used = None
        self.bugs = None
        self.text_file = None
        self.download_url = None
        self.category = None
        self.downloaded = self.check_download()

    def add_file(self):
        try:
            Database().insert_file(self)
        except sqlite3.IntegrityError:
            return False
        return True

    def check_download(self):
        file = Database().get_file_id(self.id)
        if file:
            return file[-1]
        return 0

    def __str__(self):
        return "{} - {}".format(self.id, self.title)


class Author():
    def __init__(self, id):
        self.id = id
        self.name = None

    def add_author(self):
        try:
            Database().insert_author(self)
            return True
        except sqlite3.IntegrityError:
            return False

    def __str__(self):
        return "{} - {}".format(self.id, self.name)


class Database():
    __DB_LOCATION = "./doomworld.db"

    def __init__(self):
        self.__connection = sqlite3.connect(
            self.__DB_LOCATION, check_same_thread=False
        )
        self.cursor = self.__connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS file (
                id TEXT PRIMARY_KEY UNIQUE,
                title TEXT,
                description TEXT,
                views TEXT,
                downloads TEXT,
                submitted TEXT,
                author_id INTEGER,
                credits TEXT,
                base TEXT,
                build_time TEXT,
                editors_used TEXT,
                bugs TEXT,
                text_file TEXT,
                category TEXT,
                download_url TEXT,
                downloaded INTEGER,
                FOREIGN KEY (author_id) REFERENCES author(id)
        )""")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS author (
                id TEXT PRIMARY_KEY UNIQUE,
                name TEXT
        )""")

    def insert_file(self, file):
        sql = """
            INSERT OR REPLACE INTO file (
                id, title, description, views, downloads, submitted,
                author_id, credits, base, build_time, editors_used,
                bugs, text_file, category, download_url, downloaded
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )"""
        self.cursor.execute(sql, (file.id, file.title, file.description,
                                  file.views,
                                  file.downloads, file.submitted,
                                  file.author.id, file.credits, file.base,
                                  file.build_time, file.editors_used,
                                  file.bugs, file.text_file, file.category,
                                  file.download_url, file.downloaded
                                  ))
        self.__connection.commit()

    def insert_author(self, author):
        sql = """
            INSERT INTO author (
                id, name
            ) VALUES (
                ?, ?
        )"""
        self.cursor.execute(sql, (author.id, author.name))
        self.__connection.commit()

    def get_file_id(self, file_id):
        sql = """
            SELECT * FROM file
            WHERE id = ?
        """
        self.cursor.execute(sql, (file_id, ))
        return self.cursor.fetchone()

    def set_download(self, file_id):
        sql = """
            UPDATE file
            SET downloaded = 1
            WHERE id = ?
        """
        self.cursor.execute(sql, (file_id, ))
        self.__connection.commit()

    def __del__(self):
        self.__connection.close()
