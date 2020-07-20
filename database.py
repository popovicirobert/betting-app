
import sqlite3

class DataBase:

    def __init__(self, site_name):
        self.conn = sqlite3.connect(site_name + '.db')
        self.c = self.conn.cursor()

        self.c.execute("""CREATE TABLE IF NOT EXISTS links (
                        link text PRIMARY KEY
                        )""")

        self.conn.commit()

    def delete_data(self):
        self.c.execute("DROP TABLE IF EXISTS links")
        self.conn.commit()

    def add_data(self, links):
        for link in links:
            self.c.execute("INSERT INTO links VALUES(?)", [link])
        self.conn.commit()

    def print_data(self):
        self.c.execute("SELECT * FROM links")
        return [str(link[0]) for link in self.c.fetchall()]

    def close(self):
        self.conn.close()