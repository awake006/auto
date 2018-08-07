import pymysql
from pymysql import err


class SelectMySQL(object):

    def __init__(self, host, username, password, db_name):
        self.host = host
        self.username = username
        self.password = password
        self.db_name = db_name

    def connect(self):
        try:
            self.db = pymysql.connect(self.host, self.username, self.password, self.db_name)
            self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        except err.OperationalError as e:
            raise e

    def select_one(self, select_one_sql):
        try:
            self.cursor.execute(select_one_sql)
            return self.cursor.fetchone()
        except err.InternalError as e:
            raise e
        finally:
            self.db.close()

    def select_all(self, sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except err.InternalError as e:
            raise e
        finally:
            self.db.close()


# if __name__ == "__main__":
#     db = SelectMySQL("localhost", 'root', '12346', 'test')
#     sql = "SELECT * FROM user"
#     db.connect()
#     result = db.select_all(sql)
#     print(result)