import pymssql
import json

class db:
    with open('sqlini.json', 'r') as f:
        sqlini = json.load(f)
    f.close()
    host = sqlini['host2']
    password = sqlini['password2']
    user = sqlini['user2']
    dbname = sqlini['dbname2']
    charset = 'utf8'
    database = None
    cursor = None

    def initial(self):
        db.database = pymssql.connect(host=db.host, password=db.password, user=db.user, db=db.dbname, charset=db.charset)
        db.cursor = db.database.cursor()

    def commit(self):
        db.database.commit()

    def close(self):
        db.database.close()

    def execute(self, query):
        db.cursor.execute(query)