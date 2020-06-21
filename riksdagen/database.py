import sqlite3


class Debate():
    def __init__(self, dokid):
        self.dokid = dokid
        self.title = None
        self.debateName = None
        self.debateDate = None
        self.debateType = None
        self.url = None
        self.fromChamber = None
        self.thumbnailUrl = None
        self.debateSeconds = 0
        self.streamUrl = None


class Speaker():
    def __init__(self, subid, debatesDokid):
        self.id = "{}-{}".format(debatesDokid, subid)
        self.subid = subid
        self.start = 0
        self.duration = 0
        self.text = None
        self.party = None
        self.partyCode = None
        self.active = None
        self.number = None
        self.anfText = None
        self.thumbnailUrl = None
        self.debateSeconds = 0
        self.streamUrl = None
        self.debatesDokid = debatesDokid


class Database():
    __DB_LOCATION = "./riksdagen.db"

    def __init__(self):
        self.__connection = sqlite3.connect(self.__DB_LOCATION)
        self.cursor = self.__connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS debates (
            dokid text PRIMARY_KEY UNIQUE,
            title text,
            debateName text,
            debateDate text,
            debateType text,
            url text,
            fromChamber integer,
            thumbnailUrl text,
            debateSeconds integer,
            streamUrl text,
            downloaded integer default 0
        )""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS speakers (
            id text PRIMARY_KEY UNIQUE,
            subid text,
            start integer,
            duration integer,
            text text,
            party text,
            partyCode text,
            active integer,
            number text,
            anfText text,
            thumbnailUrl text,
            debateSeconds integer,
            streamUrl text,
            debatesDokid integer NOT NULL,

            FOREIGN KEY (debatesDokid)
            REFERENCES debates(dokid)
        )""")

    def insert_debate(self, debate):
        sql = """
        INSERT INTO debates (
            dokid, title, debateName, debateDate, debateType,
            url, fromChamber, thumbnailUrl, debateSeconds, streamUrl
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )"""
        self.cursor.execute(sql, (debate.dokid, debate.title,
                            debate.debateName, debate.debateDate,
                            debate.debateType, debate.url, debate.fromChamber,
                            debate.thumbnailUrl, debate.debateSeconds,
                            debate.streamUrl))
        self.__connection.commit()

    def insert_speaker(self, speaker: Speaker):
        sql = """
        INSERT INTO speakers (
            id, subid, start, duration, text, party, partyCode, active,
            number, anfText, thumbnailUrl, debateSeconds, streamUrl,
            debatesDokid
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        );"""
        self.cursor.execute(sql, (speaker.id, speaker.subid, speaker.start,
                            speaker.duration, speaker.text, speaker.party,
                            speaker.partyCode, speaker.active, speaker.number,
                            speaker.anfText, speaker.thumbnailUrl,
                            speaker.debateSeconds, speaker.streamUrl,
                            speaker.debatesDokid))
        self.__connection.commit()

    def get_download(self):
        sql = """
        SELECT dokid, title, debateDate, streamURL, downloaded
        FROM debates
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def set_download(self, dokid):
        sql = """
        UPDATE `debates`
        SET `downloaded`=1
        WHERE dokid=?;
        """
        self.cursor.execute(sql, (dokid,))
        self.__connection.commit()

    def __del__(self):
        self.__connection.close()
