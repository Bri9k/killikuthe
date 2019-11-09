from config import KILLIDBCONFIG
import mysql.connector
from mysql.connector import errorcode
from errors import *


def killiconnection():
    try:
        cnx = mysql.connector.connect(**KILLIDBCONFIG)
        return cnx

    except mysql.connector.Error as error:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return None
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return None
        else:
            print(err)
            return None
    else:
        cnx.close()
        return None


##
# @brief Tries to execute an insert, returns error if there is an exception
# 
# @param connection a connection to the mysql server
# @param query query statement to be executed, with placeholders for parameters in order
# @param parameters parameters to be substituted in query
def exec_insert(connection, query, parameters):
    cur = connection.cursor()
    retval = 0
    try:
        cur.execute(query, parameters)
    except mysql.connector.Error as error:
        retval = error.errno
        cur.rollback()
    else:
        connection.commit()
    finally:
        cur.close()
    return retval
        



# @param connection a connection to the database
# @param MIS string, 9 digit decimal string for students
# @param first_name maximum 20 characters
# @param last_name maximum 20 characters
# @param phoneno string, a 10 digit mobile number
# @param email string, of form a@b.com maximum 45 characters
def registeruser(connection, MIS, first_name, last_name, phoneno, email):
    cur = connection.cursor()

    if len(MIS) > 9 or len(MIS) < 1:
        return MISERROR
    
    if len(first_name) > 20 or len(first_name) < 1:
        return LARGENAME

    if len(last_name) > 20 or len(last_name) < 1:
        return LARGENAME

    if not phoneno.isdigit or len(phoneno) != 10:
        return WRONGNO

    if len(email) < 10 or len(email) > 45:
        return EMAIL

    datatuple = (MIS, first_name, last_name, phoneno, email)
    add_person =  (''' INSERT INTO person '''
     ''' (MIS, first_name, last_name, mobileno, email) '''
     ''' VALUES (%s, %s, %s, %s, %s) ''')

    retval = exec_insert(connection, 
    

def addplace(connection, placename):

    cur = connection.cursor()

    if len(placename) > 40:
        return LARGENAME

    datatuple = (placename, )
    add_place = (''' INSERT INTO place '''
    ''' (name) '''
    ''' VALUES (%s) ''')

    retval = None
    try:
        cur.execute(add_place, datatuple)
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_DUP_ENTRY:
            retval = ALREADYREGISTERED
        else:
            retval = error
        connection.rollback()
    else:
        connection.commit()
    finally:
        cur.close()

    if retval:
        return retval
    return 0


def addclub(connection, clubname):

    cur = connection.cursor()

    if len(clubname) > 45:
        return LARGENAME

    datatuple = (clubname, )
    add_club = (''' INSERT INTO club '''
    ''' (clubname) '''
    ''' VALUES (%s) ''')

    retval = None
    try:
        cur.execute(add_club, datatuple)
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_DUP_ENTRY:
            retval = ALREADYREGISTERED
        else:
            retval = error
        connection.rollback()
    else:
        connection.commit()
    finally:
        cur.close()

    if retval:
        return retval
    return 0


