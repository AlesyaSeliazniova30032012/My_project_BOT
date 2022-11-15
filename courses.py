import sqlite3


class Courses:
    def __init__(self, db_file):
        self.con = sqlite3.connect(db_file)
        self.cur = self.con.cursor()
        if self.con:
            print('Соединение с БД прошло успешно!')

    def get_theway_python(self):
        with self.con:
            return self.cur.execute("SELECT description FROM 'courses' WHERE course_name='TheWayPython'").fetchone()

    def get_theway_eng(self):
        with self.con:
            return self.cur.execute("SELECT description FROM 'courses' WHERE course_name='TheWayEnglish'").fetchone()

    def get_theway_front(self):
        with self.con:
            return self.cur.execute("SELECT description FROM 'courses' WHERE course_name='TheWayFrontEnd'").fetchone()

    def get_theway_uiux(self):
        with self.con:
            return self.cur.execute("SELECT description FROM 'courses' WHERE course_name='TheWayUIUX'").fetchone()

    def get_theway_java(self):
        with self.con:
            return self.cur.execute("SELECT description FROM 'courses' WHERE course_name='TheWayJava'").fetchone()

    def get_off_python(self):
        with self.con:
            return self.cur.execute("SELECT description FROM 'courses' WHERE course_name='OfflinePython'").fetchone()

    def get_off_front(self):
        with self.con:
            return self.cur.execute("SELECT description FROM 'courses' WHERE course_name='OfflineFrontEnd'").fetchone()

    def get_off_uiux(self):
        with self.con:
            return self.cur.execute("SELECT description FROM 'courses' WHERE course_name='OfflineUIUX'").fetchone()

    def get_off_java(self):
        with self.con:
            return self.cur.execute("SELECT description FROM 'courses' WHERE course_name='OfflineJava'").fetchone()

    def get_on_python(self):
        with self.con:
            return self.cur.execute("SELECT description FROM 'courses' WHERE course_name='OnlinePython'").fetchone()

    def get_on_front(self):
        with self.con:
            return self.cur.execute("SELECT description FROM 'courses' WHERE course_name='OnlineFrontEnd'").fetchone()

    def get_on_uiux(self):
        with self.con:
            return self.cur.execute("SELECT description FROM 'courses' WHERE course_name='OnlineUIUX'").fetchone()

    def get_on_java(self):
        with self.con:
            return self.cur.execute("SELECT description FROM 'courses' WHERE course_name='OnlineJava'").fetchone()

