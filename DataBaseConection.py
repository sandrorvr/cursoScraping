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
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                isbn10 TEXT NOT NULL UNIQUE,\
                isbn13 TEXT NOT NULL UNIQUE,\
                title TEXT,\
                price TEXT,\
                author TEXT,\
                language TEXT,\
                company TEXT,\
                n_pages TEXT,\
                resume TEXT\
            )''')
        self.conn.commit()
        self.closeConection()
    
    def insertData(self, data):
        self.initConection(self.path_db)
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO _books(isbn10, isbn13, title, price, author, language, company, n_pages, resume)
                VALUES(?,?,?,?,?,?,?,?,?)
                """, data)
            self.conn.commit()
        except Exception as e:
            print('Error while louding Data Base', e.args)
        finally:
            self.closeConection()

if __name__ == '__main__':
    _db = DB()
    