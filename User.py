import sqlite3

class User:
    def __init__(self):
        self.connect = sqlite3.connect('user.db')
        print("Opened the database successfully")

    def select_all(self):
        cursor = self.connect.cursor()
        sql = "SELECT * FROM USER_TABLE"
        row = cursor.execute(sql)
        return row

    def register(self, username, password, ip, port):
        cursor = self.connect.cursor()
        try:
            sql = "INSERT INTO USER_TABLE (USERNAME,PASSWORD,STATE, IP, PORT) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(sql, (username, password, 0, ip, port))
        except sqlite3.IntegrityError:
            self.connect.rollback()
            raise ValueError("The user name already exists")
        self.connect.commit()
        print("Registration success")
        cursor.close()
        return True

    def search_username(self, username):
        cursor = self.connect.cursor()
        sql = "SELECT USERNAME, PASSWORD, STATE, IP, PORT FROM USER_TABLE WHERE USERNAME = (?)"
        cursor.execute(sql, (username,))
        row = cursor.fetchone()
        print(row)
        cursor.close()
        return row

    def login_success(self, username, ip, port):
        cursor = self.connect.cursor()
        sql = "UPDATE USER_TABLE set STATE = 1 where USERNAME = (?)"
        cursor.execute(sql, (username,))
        self.connect.commit()
        sql = "UPDATE USER_TABLE set IP = (?) where USERNAME = (?)"
        cursor.execute(sql, (ip, username,))
        self.connect.commit()
        sql = "UPDATE USER_TABLE set PORT = (?) where USERNAME = (?)"
        cursor.execute(sql, (port, username,))
        self.connect.commit()
        print(self.search_username(username))

    def login_check(self, username, password, ip, port):
        row = self.search_username(username)
        if row == None:
            print("the user is not exist")
            return False
        if password != row[1]:
            print("password is not correct")
            return False
        print(row)
        self.login_success(username, ip, port)
        return True

    def logout_success(self, username):
        cursor = self.connect.cursor()
        sql = "UPDATE USER_TABLE set STATE = 0 where USERNAME = (?)"
        cursor.execute(sql, (username,))
        self.connect.commit()

    def db_close(self):
        self.connect.close()