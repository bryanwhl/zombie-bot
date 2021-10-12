import sqlite3
import threading
import random, string
import Constants as keys
import requests

'''
CONSTANTS
'''
LOCK = threading.Lock()
FULL_NAME = 0
USERNAME = 1
HOUSE = 2
TELEGRAM_ID = 3
CODE = 4
IS_HUMAN = 5
POINTS = 6

class Database:
    '''
    Initializing database.db file and connecting to the file
    '''
    def __init__(self):
        self.con = sqlite3.connect(
            'database.db', check_same_thread=False)
        self.cur = self.con.cursor()

    '''
    Initializing commit function
    '''
    def commit(self):
      self.con.commit()

    '''
    Initializing tables which only needs to be called once at the start of the program
    '''
    def create_tables(self):
        try:
            self.cur.execute(
                '''CREATE TABLE users(full_name text, username text, house text, telegram_id text, code text, is_human text, points integer, telegram_handle text)''')
            self.cur.execute(
                '''CREATE TABLE code_submissions(code1 text, code2 text)''')
            self.cur.execute(
                '''CREATE TABLE admins(telegram_id text)''')
            self.con.commit()
            return True
        except Exception as e:
            print(e)
            return e

    def full_name_exist(self, full_name):
        try:
            self.cur.execute("SELECT * FROM users WHERE full_name=?", (full_name,))
            if (len(self.cur.fetchall())):
                return True
            return False

        except Exception as e:
            print(e)
            return e            

    def username_exist(self, username):
        try:
            self.cur.execute("SELECT * FROM users WHERE username=?", (username,))
            if (len(self.cur.fetchall())):
                return True
            return False
            
        except Exception as e:
            print(e)
            return e
    
    def telegram_id_exist(self, telegram_id):
        try:
            self.cur.execute("SELECT * FROM users WHERE telegram_id=?", (telegram_id,))
            if (len(self.cur.fetchall())):
                return True
            return False
        
        except Exception as e:
            print(e)
            return e

    def generate_code(self):
        try:
            while True:
                code = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
                self.cur.execute("SELECT * FROM users WHERE code=?", (code,))
                if (len(self.cur.fetchall()) == 0):
                    break
            return code

        except Exception as e:
            print(e)
            return e

    def assign_role(self, house):
        # 0 for zombie, 1 for human
        try:
            self.cur.execute("SELECT * FROM users WHERE is_human=? AND house=?", (1, house,))
            no_humans = len(self.cur.fetchall())
            self.cur.execute("SELECT * FROM users WHERE is_human=? AND house=?", (0, house))
            no_zombies = len(self.cur.fetchall())
            # return 1
            if (no_zombies * 5 > no_humans):
                return 1
            else:
                return 0
        except Exception as e:
            print(e)
            return e
            
    def insert_user(self, full_name, username, house, telegram_id, code, is_human, points, telegram_handle):
        try:

            # ## if telegram_id registered before, delete and insert
            # self.cur.execute("SELECT * FROM users WHERE telegram_id=?", (telegram_id,))
            # rows = self.cur.fetchall()
            # if (len(rows)):
            #     name = rows[0][USER_NAME]
            #     self.cur.execute(
            #     "DELETE FROM users WHERE telegram_id=?", (telegram_id,))

            #     ## update details of user
            #     self.cur.execute("UPDATE events_joined SET username=? WHERE telegram_id=?", (username, telegram_id))
            #     # self.cur.execute("UPDATE user_feedback SET username=? WHERE telegram_id=?", (username, telegram_id))

            self.cur.execute("INSERT INTO users(full_name, username, house, telegram_id, code, is_human, points, telegram_handle) VALUES(?,?,?,?,?,?,?,?)",
                             (full_name, username, house, telegram_id, code, is_human, points, telegram_handle))
            self.con.commit()
            return True
        except Exception as e:
            print(e)
            return e

    def query_all_users(self):
        try:
            self.cur.execute("SELECT * from users")
            rows = self.cur.fetchall()
            arrayString = []
            for row in rows:
                arrayString.append(row)
            return arrayString
        except Exception as e:
            print(e)
            return e

    def query_user(self, telegram_id):
        try:
            self.cur.execute("SELECT * from users WHERE telegram_id=?", (telegram_id,))
            rows = self.cur.fetchall()
            arrayString = []
            for row in rows[0]:
                arrayString.append(row)
            return arrayString
        except Exception as e:
            print(e)
            return e

    def delete_user(self, full_name):
        try:
            self.cur.execute(
                "DELETE FROM users WHERE full_name=?", (full_name,))
            self.con.commit()

        except Exception as e:
            print(e)
            return e

    def submit_code(self, telegram_id, code):
        # 0 - code does not exist
        try:
            token = keys.API_KEY
            token_admin = keys.API_KEY_ADMIN

            # submit code
            self.cur.execute("SELECT * from users WHERE telegram_id=?", (telegram_id,))
            user_details = self.cur.fetchall()[0]
            p1_role = user_details[IS_HUMAN]
            p1_points = user_details[POINTS]
            p1_username = user_details[USERNAME]
            p1_telegram_id = user_details[TELEGRAM_ID]
            p1_code = user_details[CODE]
            p1_full_name = user_details[FULL_NAME]
            
            # give code
            self.cur.execute("SELECT * from users WHERE code=?", (code,))
            array = self.cur.fetchall()
            if (len(array) == 0):
                return 0
            user_details = array[0]
            p2_role = user_details[IS_HUMAN]
            p2_points = user_details[POINTS]
            p2_username = user_details[USERNAME]
            p2_telegram_id = user_details[TELEGRAM_ID]
            p2_code = user_details[CODE]
            p2_full_name = user_details[FULL_NAME]            

            if (p1_telegram_id == p2_telegram_id):
                return -1
            
            self.cur.execute("SELECT * FROM code_submissions WHERE code1=?", (p1_code,))
            pairs = self.cur.fetchall()
            if (len(pairs)):
                for pair in pairs:
                    p1_pair = pair[1]
                    if (p1_pair == p2_code):
                        return -2


            self.cur.execute("SELECT * FROM code_submissions WHERE code1=?", (p2_code,))
            pairs = self.cur.fetchall()
            if (len(pairs)):
                for pair in pairs:
                    p2_pair = pair[1]
                    if (p2_pair == p1_code):
                        return -2

            self.cur.execute("INSERT INTO code_submissions(code1, code2) VALUES(?,?)", (p1_code, p2_code))
            self.con.commit()


            self.cur.execute("SELECT * from admins")
            rows = self.cur.fetchall()
            message = p1_full_name + " submitted " + p2_full_name + "'s code."
            for row in rows:
                url_req = "https://api.telegram.org/bot" + token_admin + "/sendMessage" + "?chat_id=" + row[0] + "&text=" + message 
                results = requests.get(url_req)

            # human submit human
            if (p1_role == '1' and p2_role == '1'): 
                p1_points += 5
                p2_points += 5
                self.cur.execute("UPDATE users SET points=? WHERE telegram_id=?", (p1_points, p1_telegram_id))
                self.con.commit()
                self.cur.execute("UPDATE users SET points=? WHERE telegram_id=?", (p2_points, p2_telegram_id))
                self.con.commit()

                # send message to player 2
                message = "Your fellow human, " + p1_username + ", have submitted your code. Added 5 points."
                url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + str(p2_telegram_id) + "&text=" + message 
                results = requests.get(url_req)
                return 1

            # human submit zombie
            if (p1_role == '1' and p2_role == '0'):
                p1_points = 0
                p2_points += 10
                self.cur.execute("UPDATE users SET points=? WHERE telegram_id=?", (p1_points, p1_telegram_id))
                self.con.commit()
                self.cur.execute("UPDATE users SET is_human=? WHERE telegram_id=?", (p2_role, p1_telegram_id))
                self.con.commit()
                self.cur.execute("UPDATE users SET points=? WHERE telegram_id=?", (p2_points, p2_telegram_id))
                self.con.commit()

                # send message to player 2
                message = "Nice work tricking " + p1_username + "! Added 10 points."
                url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + str(p2_telegram_id) + "&text=" + message 
                results = requests.get(url_req)
                return 2

            # zombie submit human
            if (p1_role == '0' and p2_role == '1'):
                p1_points += 10
                p2_points = 0
                self.cur.execute("UPDATE users SET points=? WHERE telegram_id=?", (p1_points, p1_telegram_id))
                self.con.commit()
                self.cur.execute("UPDATE users SET points=? WHERE telegram_id=?", (p2_points, p2_telegram_id))
                self.con.commit()
                self.cur.execute("UPDATE users SET is_human=? WHERE telegram_id=?", (p1_role, p2_telegram_id))
                self.con.commit()

                # send message to player 2
                message = "Yikes! You have been zombified by " + p1_username + ". Welcome to the evil side. Your points have been resetted."
                url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + str(p2_telegram_id) + "&text=" + message 
                results = requests.get(url_req)
                return 3

            # zombie submit zombie
            if (p1_role == '0' and p2_role == '0'):
                return 4

        except Exception as e:
            print(e)
            return e

    def query_code_submissions_table(self):
        try:
            self.cur.execute("SELECT * FROM code_submissions")
            rows = self.cur.fetchall()
            arrayString = []
            for row in rows:
                arrayString.append(row)
            return arrayString
        except Exception as e:
            print(e)
            return e

    def query_number_humans(self):
        try:
            self.cur.execute("SELECT COUNT(*) FROM users WHERE is_human=?", ('1'))
            number = self.cur.fetchall()[0][0]
            return number
        except Exception as e:
            print(e)
            return e

    def query_number_zombies(self):
        try:
            self.cur.execute("SELECT COUNT(*) FROM users WHERE is_human=?", ('0'))
            number = self.cur.fetchall()[0][0]
            return number
        except Exception as e:
            print(e)
            return e

    def query_top_usernames(self, number):
        try:
            self.cur.execute("SELECT * FROM users ORDER BY points DESC")
            rows = self.cur.fetchall()
            arrayString = []
            if (len(rows) < number):
                number = len(rows)
            for i in range(number):
                arrayString.append(rows[i][USERNAME])
            return arrayString

        except Exception as e:
            print(e)
            return e

    def insert_admin(self, telegram_id):
        try:
            self.cur.execute("SELECT * FROM admins WHERE telegram_id=?", (telegram_id,))
            if (len(self.cur.fetchall())):
                return
            self.cur.execute("INSERT INTO admins(telegram_id) VALUES(?)", (telegram_id,))
            self.con.commit()
            return
        
        except Exception as e:
            print(e)
            return e

    def query_all_admins(self):
        try:
            self.cur.execute("SELECT * from admins")
            rows = self.cur.fetchall()
            arrayString = []
            for row in rows:
                arrayString.append(row)
            return arrayString[0][0]
        except Exception as e:
            print(e)
            return e
