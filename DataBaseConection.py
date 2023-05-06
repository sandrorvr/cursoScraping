import sqlite3
class DB:
    conn = None

    def __init__(self, path_db='db.sqlite'):
        self.path_db = path_db
        self.t = 0
    
    @classmethod
    def initConection(cls, path_db):
        cls.conn = sqlite3.connect(path_db)

    def closeConection(self):
        self.conn.close()
    
    def createDB(self):
        self.initConection(self.path_db)
        cursor = self.conn.cursor()
        cursor.execute('''\
            CREATE TABLE IF NOT EXISTS _books\
            (\
                id INTEGER NOT NULL PRIMARY KEY,\
                title TEXT,\
                price TEXT,\
                authors TEXT\
            )''')
        self.conn.commit()
        self.closeConection()
    
    def insertData(self, data):
        self.initConection(self.path_db)
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO _books(id, title, price, authors)
            VALUES(?,?,?,?)
            """, data)
        self.conn.commit()
        self.closeConection()

if __name__ == '__main__':
    _db = DB()
    