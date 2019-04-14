import sqlite3

class con_db:
    def __init__(self):
        self.database = "arzaq.db"
        self.mydb = sqlite3.connect(self.database)
        self.mycursor = self.mydb.cursor()


    def query(self, x):
        self.mycursor.execute(x)
        return list(self.mycursor)

