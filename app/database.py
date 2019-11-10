import mysql.connector
from mysql.connector import errorcode

class database:
    def __init__(self, dbconfig):
        self.cnx = None
        self.latestrowcount = 0
        self.lastrowid = 0
        try:
            self.cnx = mysql.connector.connect(**dbconfig)
        except mysql.connector.Error as error:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)


    ##
    # @brief Tries to execute an insert, returns error if there is an exception
    # 
    # @param connection a connection to the mysql server
    # @param query query statement to be executed, with placeholders for parameters in order
    # @param parameters parameters to be substituted in query
    def exec_insert(self, query, parameters):
        cur = self.cnx.cursor()
        retval = 0
        try:
            cur.execute(query, parameters)
        except mysql.connector.Error as error:
            print(error)
            retval = error.errno
            self.cnx.rollback()
        else:
            print("Commited")
            self.cnx.commit()
            self.lastrowid = cur.lastrowid
            self.latestrowcount = cur.rowcount
        finally:
            cur.close()
        return retval

    def query(self, query, parameters):
        cur = self.cnx.cursor()

        cur.execute(query, parameters)

        return cur.fetchall()


    def commit(self):
        self.cnx.commit()

    def rollback(self):
        self.cnx.rollback()

    def run_modification(self, query, parameters):
        cur = self.cnx.cursor()
        try:
            cur.execute(query, parameters)
        except mysql.connector.Error as error:
            retval = error.errno
        else:
            retval = 0
            self.lastrowid = cur.lastrowid
            self.latestrowcount = cur.rowcount
        finally:
            cur.close()
        return retval



