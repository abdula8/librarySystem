import MySQLdb
import mysql.connector
import logging

class DbOperations:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.connect_db()

    def connect_db(self):
        try:
            self.conn = mysql.connector.connect(host='localhost', user='root', password='01099110790aA@', db='library')
            print('Connection Accepted')
            # self.cur = self.db.cursor()
            self.cur = self.conn.cursor()
            logging.info("Database connection established successfully.")
        except mysql.connector.Error as err:
            logging.error(f"Error: {err}")
            self.conn = None
            self.cur = None


    # def execute_query(self, query, params=()):
    #     self.cur.execute(query, params)
    #     return self.cur.fetchall()

    def execute_query(self, query, params=None):
        if self.cur is not None:
            try:
                self.cur.execute(query, params)
                return self.cur.fetchall()
            except mysql.connector.Error as err:
                logging.error(f"Query Error: {err}")
                return None
        else:
            logging.error("Database connection is not initialized.")
            return None
    def __del__(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()
    def commit(self):
        self.conn.commit()
