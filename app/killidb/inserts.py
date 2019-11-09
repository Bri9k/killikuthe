import mysql.connector
from mysql.connector import errorcode
from errors import *


class database:
    def __init__(self, dbconfig):
        self.cnx = None
        self.latestrowcount = 0
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
            self.lastid = cur.lastrowid
            self.latestrowcount = cur.rowcount
        finally:
            cur.close()
        return retval

    def query(self, query, parameters):
        cur = self.cnx.cursor()

        cur.execute(query, parameters)

        return cur.fetchall()


    def commit(self):
        print("Commit")
        self.cnx.commit()

    def rollback(self):
        self.cnx.rollback()

    def run_modification(self, query, parameters):
        cur = self.cnx.cursor()
        try:
            cur.execute(query, parameters)
        except mysql.connector.Error as error:
            retval = error.errno
            self.cnx.rollback()
        else:
            retval = 0
            self.lastid = cur.lastrowid
            self.latestrowcount = cur.rowcount
        finally:
            cur.close()
        return retval


# @param connection a connection to the database
# @param MIS string, 9 digit decimal string for students
# @param first_name maximum 20 characters
# @param last_name maximum 20 characters
# @param phoneno string, a 10 digit mobile number
# @param email string, of form a@b.com maximum 45 characters
def registeruser(db, MIS, first_name, last_name, phoneno, email):

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
    add_person =  (''' INSERT INTO person
                       (MIS, first_name, last_name, mobileno, email)
                       VALUES (%s, %s, %s, %s, %s) ''')

    retval = 0
    retval = db.exec_insert(add_person, datatuple)
    return retval
    

def registerplace(db, placename, store = False, studentaccess = False):

    if len(placename) > 40:
        return LARGENAME

    datatuple = (placename, store)
    add_place = (''' INSERT INTO place
                     (name, store)
                     VALUES (%s, %s) ''')

    retval = 0
    retval = db.exec_insert(add_place, datatuple)
    if retval == errorcode.ER_DUP_ENTRY:
        retval = ALREADYREGISTERED
    return retval


def registerclub(db, clubname, managed_by):


    if len(clubname) > 45:
        return LARGENAME

    datatuple = (clubname, managed_by)
    add_club = (''' INSERT INTO club 
                    (clubname, managed_by)
                    VALUES (%s, %s) ''')

    retval = db.exec_insert(add_club, datatuple)
    if retval == errorcode.ER_DUP_ENTRY:
        retval = ALREADYREGISTERED
    return retval


def changemanager(db, cid, new_manager):

    if len(new_manager) < 1 or len(new_manager) > 10:
        return  MISERROR

    datatuple = (new_manager, cid)
    #check_membership = ('''SELECT true '''
    #                   '''WHERE "%s" IN '''
    #                   '''(SELECT person_MIS '''
    #                   '''FROM person_memberof_club AS M'''
    #                   '''WHERE M.club_cid = %d)''')
    #res = db.query(check_membership, datatuple)
    #print(res[1])
    #if res[0][0] != 0:
    #    return res[0][0]
    #elif res[1][0] == False:
    #    return NOTMEMBER
    change_manager = ('''UPDATE club
                         SET managed_by = %s 
                         WHERE cid = %s ''')

    retval = 0
    retval = db.exec_insert(change_manager, datatuple)
    return retval

def addclubmember(db, cid, member_MIS):

    datatuple = (cid, member_MIS)
    add_member = (''' INSERT INTO person_memberof_club
                    (club_cid, person_MIS)
                    VALUES (%s, %s) ''')

    retval = 0
    retval = db.exec_insert(add_member, datatuple)

    if retval == errorcode.ER_DUP_ENTRY:
        return ALREADYREGISTERED
    else:
        return retval

def addkey(db, place_pid, store_pid = None):
    if store_pid == None:
        store_pid = place_pid
    else:
        print("Entered Else")
        datatuple = (store_pid, )
        check_whether_store = ('''SELECT store
                                  FROM place
                                  WHERE pid = %s''')
        output = db.query(check_whether_store, datatuple)
        print(output)
        if len(output) == 0: # storage place invalid
            return NOTASTORAGEPLACE

  
    datatuple = [place_pid]
    find_no_of_keys = ('''SELECT COUNT(*) 
                          FROM killi 
                          WHERE place_pid = %s ''')

    result = db.query(find_no_of_keys, datatuple)
    print("Reached here")
    kitikillya = result[0][0]


    datatuple = (place_pid, store_pid)
    keydata = (kitikillya + 1, place_pid, None, store_pid)
    add_key = ('''INSERT INTO killi
                  (kid, place_pid, person_MIS, place_pid_store)
                  VALUES (%s, %s, %s, %s) ''')
    retval = db.exec_insert(add_key, keydata)
    return retval


def grantkeypermission(db, club_cid, place_pid, key_kid):
    
    datatuple = (club_cid, key_kid, place_pid)
    permissionentry = ('''INSERT INTO club_canuse_key
                          (club_cid, key_kid, key_place_pid)
                          VALUES (%s, %s, %s) ''')
    
    retval = db.exec_insert(permissionentry, datatuple)
    if retval == errorcode.ER_NO_REFERENCED_ROW_2:
        retval = KEYDOESNOTEXIST
    elif retval == errorcode.ER_DUP_ENTRY:
        retval = ALREADYREGISTERED
    return retval


def person_canuse_key(db, person_MIS, place_pid, key_kid):
        datatuple = (person_MIS, place_pid, key_kid)
        canaccesskey = ('''SELECT COUNT(*) 
                           FROM person_memberof_club M INNER JOIN club_canuse_key U
                           ON M.club_cid = U.club_cid 
                           WHERE %s = M.person_MIS 
                           AND (%s, %s) = (U.key_place_pid, U.key_kid)''')
        total = db.query(canaccesskey, datatuple)
        print(total)

        return total[0][0] == 1
        

def pickup_key(db, person_MIS, place_pid, key_kid):
    datatuple = (person_MIS, key_kid, place_pid)
    change_holdership = ('''UPDATE killi 
                            SET person_MIS = %s, 
                                place_pid_store = NULL 
                            WHERE (kid, place_pid) = (%s, %s) 
                            AND person_MIS IS NULL
                            AND place_pid_store IS NOT NULL''')

    retval = db.exec_insert(change_holdership, datatuple)
    
    if retval == 0 and db.latestrowcount == 0:
        print(db.latestrowcount)
        retval = INVALIDKEY

    return retval


def place_key(db, person_MIS, place_pid, key_kid, where_pid):

    if not where_pid == place_pid:
        datatuple = (where_pid,)
        isstorage = ('''SELECT COUNT(*)
                        FROM place
                        WHERE pid = %s AND store = TRUE''')
        total = db.query(isstorage, datatuple)
        is_storage = total[0][0] == 1

        if not is_storage:
            return CANNOTPLACETHERE

    datatuple = (where_pid, place_pid, key_kid, person_MIS)
    putkey = ('''UPDATE killi
                 SET person_MIS = NULL,
                     place_pid_store = %s
                 WHERE (place_pid, kid) = (%s, %s) and person_MIS = %s''')
    retval = db.exec_insert(putkey, datatuple)
    if retval == 0 and db.latestrowcount == 0:
        retval = DONOTHAVEKEY
    elif retval == 0:
        # delete all pending requests- person can no longer fulfill them
        deleterequests = ('''DELETE 
                             FROM request_key
                             WHERE (key_id, place_pid) = (%s, %s)''')
        datatuple = (key_kid, place_pid)
        db.exec_insert(deleterequests, datatuple)

    return retval


# note that user has to be shown who possess the key- but only person and key are requried to identify it 
def request_key(db, person_MIS, place_pid, key_kid):
    if not person_canuse_key(db, person_MIS, place_pid, key_kid):
        return CANNOTUSE

    keyheld = ('''SELECT COUNT(*)
                  FROM killi
                  WHERE (kid, place_pid) = (%s, %s) AND person_MIS IS NOT NULL and NOT(person_MIS = %s)''')
    datatuple = (key_kid, place_pid, person_MIS)
    total = db.query(keyheld, datatuple)
    print("Total", total)
    personholds = total[0][0] == 1
    if not personholds:
        return INVALIDREQUEST

    makerequest = ('''INSERT INTO request_key
                      (destination, place_pid, key_id)
                      VALUES (%s, %s, %s)''')
    datatuple = (person_MIS, place_pid, key_kid)

    retval = db.exec_insert(makerequest, datatuple)
    if retval == errorcode.ER_DUP_ENTRY:
        retval = ALREADYREGISTERED

    return retval

# note that request is only visible to person who has the key, so only that person can press the button. So there is no 'source' argument
def transfer_key(db, destination_person_MIS, place_pid, key_kid):

    holdershipupdate = ('''UPDATE killi
                           SET person_MIS = %s
                           WHERE (place_pid, kid) = (%s, %s)''')
    datatuple = (destination_person_MIS, place_pid, key_kid)

    retval = db.run_modification(holdershipupdate, datatuple)
    if retval != 0:
        return retval

    requestremove = ('''DELETE
                        FROM request_key
                        WHERE (destination, place_pid, key_id) = (%s, %s, %s)''')
    datatuple = (destination_person_MIS, place_pid, key_kid)
    
    retval = db.run_modification(requestremove, datatuple)
    
    if retval == 0 and db.latestrowcount != 1:
        db.rollback()
        retval = TRANSFERWITHOUTREQUEST
    elif retval == 0:
        db.commit()

    return retval




