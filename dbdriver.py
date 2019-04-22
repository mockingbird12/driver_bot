import psycopg2
import config
import os


class UserStatus():
    # conn = psycopg2.connect("host='localhost' dbname='telegram_bot_db' user='pythonspot' password='111111'")
    conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
    conn.set_client_encoding('UTF8')
    cur = conn.cursor()
    sql = "CREATE TABLE IF NOT EXISTS user_state (id SERIAL PRIMARY KEY, user_id VARCHAR(20), " \
                                                            "state VARCHAR(20), user_type VARCHAR(20))"
    cur.execute(sql)
    conn.commit()

    def __init__(self):
        self.user_id = None
        self.user_type = None

    def user_exsist(self):
        sql = 'SELECT * FROM user_state WHERE user_id = %s'
        data = (str(self.user_id),)
        self.cur.execute(sql, data)
        res = self.cur.fetchall()
        if res: return True
        else: return False

    def _delete_old_status(self):
        if self.user_exsist():
            sql = "DELETE FROM user_state WHERE user_id = %s"
            data = (str(self.user_id),)
            self.cur.execute(sql,data)

    def _add_new_status(self, state):
        if not self.user_exsist():
            if self.user_id == None: raise Exception("user_id None")
            sql = "INSERT INTO user_state (user_id, state, user_type) VALUES (%s, %s, %s)"
            data = (self.user_id, state, self.user_type)
            self.cur.execute(sql, data)

    def set_status(self, state):
        self._delete_old_status()
        self._add_new_status(state)
        self.conn.commit()

    def set_type(self, type):
        if self.user_id == None: raise Exception("user id empty")
        sql = "INSERT INTO user_state (user_type) VALUES (%s) WHERE user_id = %s"
        data = (type, self.user_id)
        self.cur.execute(sql, data)
        self.conn.commit()

    def get_type(self):
        sql = "SELECT user_type FROM user_state WHERE user_id = %s"
        data = (self.user_id,)
        self.cur.execute(sql, data)
        res = self.cur.fetchall()[0][0]
        return res

    @classmethod
    def get_status(self, user_id):
        sql = "SELECT state FROM user_state WHERE user_id = %s"
        data = (str(user_id),)
        self.cur.execute(sql, data)
        res = self.cur.fetchall()
        if res:
            return res[0][0]
        else: return None

    def delete_user(self):
        self._delete_old_status()
        self.conn.commit()


class Loaders:
    # conn = psycopg2.connect("host='localhost' dbname='telegram_bot_db' user='pythonspot' password='111111'")
    conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
    conn.set_client_encoding('UTF8')
    cur = conn.cursor()
    sql = "CREATE TABLE IF NOT EXISTS loaders (id SERIAL PRIMARY KEY, user_id VARCHAR(20) UNIQUE, " \
          "fio VARCHAR(20), district VARCHAR(40), passport_foto VARCHAR(140), person_foto VARCHAR(140), isAccept VARCHAR(20))"
    cur.execute(sql)
    conn.commit()

    def check_exsist(self, user_id):
        sql = 'SELECT * FROM loaders WHERE user_id = %s'
        data = (str(user_id),)
        self.cur.execute(sql, data)
        res = self.cur.fetchall()
        if res:
            return True
        else:
            return False

    def insert_data(self, user_id, data):
        if user_id == None: raise Exception("user_id None")
        sql = "INSERT INTO loaders (user_id, fio, district, passport_foto, person_foto, isaccept) VALUES " \
              "(%s, %s, %s, %s, %s, %s)"
        data_sql = (user_id, data.get('fio'), data.get('district'), data.get('passport_foto'), data.get('person_foto'),
                    config.WAITING)
        print (self.cur.mogrify(sql, data_sql))
        self.cur.execute(sql, data_sql)
        self.conn.commit()

    def get_accept_status(self, user_id):
        sql = "SELECT isaccept FROM loaders"
        data = (user_id,)
        self.cur.execute(sql, data)
        res = self.cur.fetchall()[0][0]
        return res

    def delete(self, user_id):
        sql = "DELETE FROM loaders WHERE user_id = %s"
        data = (str(user_id),)
        self.cur.execute(sql, data)
        self.conn.commit()
