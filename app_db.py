import sqlite3
import pandas as pd

class Database:
    def __init__(self):
        self.dbname = "./db/card.db"
        self.conn = None
        self.cursor = None

    def get_words(self):
        sql = "SELECT * FROM word"
        conn = sqlite3.connect(self.dbname)
        df = pd.read_sql_query(sql, conn)
        conn.close()
        df = df.sample(frac=1).reset_index(drop=True)
        return df


def sample():
    db = Database()
    words = db.get_words()
    print(words.head())

if __name__ == "__main__":
    sample()