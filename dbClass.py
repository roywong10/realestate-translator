import pymssql
import json

class db:
    with open('config.json', 'r') as f:
        sqlini = json.load(f)
    f.close()
    host = sqlini['host']
    password = sqlini['password']
    user = sqlini['user']
    dbname = sqlini['dbname']
    charset = 'utf8'
    database = None
    cursor = None

    def __init__(self):
        db.database = pymssql.connect(host=db.host, password=db.password, user=db.user, database=db.dbname, charset=db.charset)
        db.cursor = db.database.cursor()

    def commit(self):
        db.database.commit()

    def close(self):
        db.database.close()

    def execute(self, query):
        db.cursor.execute(query)