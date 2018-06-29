import pymssql
import json

class db:
    with open('config.json', 'r') as f:
        sqlini = json.load(f)['sql']
    f.close()
    host = sqlini['host']
    password = sqlini['password']
    user = sqlini['user']
    database = sqlini['database']
    charset = 'utf8'
    conn = None
    cursor = None

    def __init__(self):
        self.conn = pymssql.connect(host=self.host, password=db.password, user=db.user, database=db.database, charset=db.charset)
        self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def execute(self, query):
        self.cursor.execute(query)


if __name__ == '__main__':
    db = db()
    sql = "select top 1 * from sys.tables"
    db.execute(sql)
    result = db.cursor.fetchall()
    print(result)

