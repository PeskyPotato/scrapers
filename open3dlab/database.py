import sqlite3


class Project():
    def __init__(self, id):
        self.id = id
        self.title = None
        self.description = None
        self.images = []
        self.user = None
        self.posted = None
        self.views = None
        self.category = None
        self.licence = 0
        self.downloads = []

    def add_project(self):
        try:
            Database().insert_project(self)
            for image in self.images:
                Database().insert_image(image, self.id)
        except sqlite3.IntegrityError:
            return False
    
    def __str__(self):
        return "{} - {}".format(self.id, self.title)


class User():
    def __init__(self, id):
        self.id = id
        self.name = None

    def add_user(self):
        try:
            Database().insert_user(self)
            return True
        except sqlite3.IntegrityError:
            return False

class Download():
    def __init__(self, filename):
        self.filename = filename
        self.downloads = None
        self.created = None
        self.filesize = None
        self.urls = []
        self.project_id = None

    def add_download(self):
        db = Database()
        try:
            download_id = db.insert_download(self)
            for url in self.urls:
                db.insert_download_url(url, download_id)
            return True
        except sqlite3.IntegrityError:
            return False

class Database():
    __DB_LOCATION = "./smutbase.db"

    def __init__(self):
        self.__connection = sqlite3.connect(self.__DB_LOCATION)
        self.cursor = self.__connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS project (
                id INTEGER PRIMARY_KEY UNIQUE,
                title TEXT,
                description TEXT,
                user_id INTEGER,
                posted TEXT,
                views TEXT,
                category TEXT,
                licence TEXT,
                downloaded INTEGER default 0,
                FOREIGN KEY (user_id) REFERENCES user(id)
        )""")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS image (
                id INTEGER PRIMARY KEY ASC,
                url TEXT,
                project_id INTEGER,
                FOREIGN KEY (project_id) REFERENCES project(id)
        )""")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY_KEY UNIQUE,
                name TEXT
        )""")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS download (
                id INTEGER PRIMARY KEY ASC,
                filename TEXT,
                downloads TEXT,
                created TEXT,
                filesize TEXT,
                project_id INTEGER,
                downloaded INTEGER default 0,
                FOREIGN KEY (project_id) REFERENCES project(id)
        )""")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS download_url (
                id INTEGER PRIMARY KEY ASC,
                url TEXT,
                download_id INTEGER,
                FOREIGN KEY (download_id) REFERENCES download(id)
        )""")

    def insert_project(self, project):
        sql = """
            INSERT INTO project (
                id, title, description, user_id, posted,
                views, category, licence
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?
        )"""
        self.cursor.execute(sql, (project.id, project.title, project.description,
                                    project.user.id, project.posted,
                                    project.views, project.category, project.licence))
        self.__connection.commit()

    def insert_user(self, user):
        sql = """
            INSERT INTO user (
                id, name
            ) VALUES (
                ?, ?
        )"""
        self.cursor.execute(sql, (user.id, user.name))
        self.__connection.commit()

    def insert_download(self, download):
        sql = """
            INSERT INTO download (
                filename, downloads, created, filesize, project_id
            ) VALUES (
                ?, ?, ?, ?, ?
        )"""
        self.cursor.execute(sql, (download.filename, download.downloads,
                                    download.created, download.filesize,
                                    download.project_id))
        self.__connection.commit()
        return self.cursor.lastrowid

    def insert_download_url(self, url, download_id):
        sql = """
            INSERT INTO download_url (
                url, download_id
            ) VALUES (
                ?, ?
        )"""
        self.cursor.execute(sql, (url, download_id))
        self.__connection.commit()

    def insert_image(self, url, project_id):
        sql = """
            INSERT INTO image (
                url, project_id
            ) VALUES (
                ?, ?
        )"""
        self.cursor.execute(sql, (url, project_id))
        self.__connection.commit()

    def get_not_downloaded_download(self):
        sql = """
            SELECT * FROM download
            WHERE downloaded = 0
        """
        self.cursor.execute(sql, )
        return self.cursor.fetchall()

    def get_url(self, id):
        sql = """
            SELECT * FROM download_url
            WHERE download_id = ?
        """
        self.cursor.execute(sql, (id, ))
        return self.cursor.fetchall()

    def set_download_download(self, id):
        sql = """
            UPDATE `download`
            SET `downloaded`=1
            WHERE id=?;
        """
        self.cursor.execute(sql, (id,))
        self.__connection.commit()

    def get_not_downloaded_project(self):
        sql = """
            SELECT * FROM project
            WHERE downloaded = 0
        """
        self.cursor.execute(sql, )
        return self.cursor.fetchall()

    def get_image_urls(self, id):
        sql = """
            SELECT * FROM image
            WHERE project_id = ?
        """
        self.cursor.execute(sql, (id, ))
        return self.cursor.fetchall()

    def set_download_project(self, id):
        sql = """
            UPDATE `project`
            SET `downloaded`=1
            WHERE id=?;
        """
        self.cursor.execute(sql, (id,))
        self.__connection.commit()

    def get_project(self, id):
        sql = """
            SELECT * FROM project
            WHERE id = ?;
        """
        self.cursor.execute(sql, (id,))
        return self.cursor.fetchone()

    def __del__(self):
        self.__connection.close()
