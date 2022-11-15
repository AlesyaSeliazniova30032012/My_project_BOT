import sqlite3


class Database:
    def __init__(self, db_file):
        self.con = sqlite3.connect(db_file)
        self.cur = self.con.cursor()
        if self.con:
            print('Соединение с БД прошло успешно!')

    async def create_table(self):
        with self.con:
            return self.cur.execute("CREATE TABLE IF NOT EXISTS 'profile' (user_id INTEGER NOT NULL, name TEXT, "
                                    "login TEXT, password TEXT, email TEXT, sign_up TEXT DEFAULT 'setlogin', "
                                    "time_subscribe INTEGER NOT NULL DEFAULT 0, active INTEGER DEFAULT 1)")

    async def add_profile(self, state, user_id):
        with self.con:
            async with state.proxy() as data:
                return self.cur.execute("INSERT INTO 'profile' (user_id, name, login, password, email) "
                                        "VALUES (?, ?, ?, ?, ?)", (user_id, data['name'], data['login'],
                                                                   data['password'], data['email']))

    def user_exists(self, user_id):
        with self.con:
            result = self.cur.execute("SELECT * FROM 'profile' WHERE user_id=?", (user_id,)).fetchall()
            return bool(len(result))

    def get_user(self, user_id):
        with self.con:
            result = self.cur.execute("SELECT * FROM 'profile' WHERE user_id=?", (user_id,)).fetchall()

            for entry in result:
                user_id = str(entry[0])
                user_name = str(entry[1])
                user_login = str(entry[2])
                user_password = str(entry[3])
                user_email = str(entry[4])
                return f'Твой ID: {user_id}\n' \
                       f'Твое имя: {user_name}\n' \
                       f'Твой логин: {user_login}\n' \
                       f'Твой пароль: {user_password}\n' \
                       f'Твой e-mail: {user_email}'

    def get_sign_up(self, user_id):
        with self.con:
            result = self.cur.execute("SELECT sign_up FROM 'profile' WHERE user_id=?", (user_id,)).fetchall()

            for entry in result:
                sign_up = str(entry[0])
                return sign_up

    def set_sign_up(self, user_id, sign_up):
        with self.con:
            return self.cur.execute("UPDATE profile SET sign_up=? WHERE user_id=?", (sign_up, user_id,))

    def set_active(self, user_id, active):
        with self.con:
            return self.cur.execute("UPDATE 'profile' SET active=? WHERE user_id=?", (active, user_id,))

    # для рассылки
    def get_users(self):
        with self.con:
            return self.cur.execute("SELECT user_id, active FROM 'profile'").fetchall()
