from errors import *
from mysql.connector import errorcode


def getplaces(db):
    
    search = '''SELECT pid, name, store
              FROM place
              ORDER BY name'''
    parameters = None
    places_list = db.query(search, parameters)
    return places_list

def getclubs(db):
    search = '''SELECT cid, clubname, P.MIS, P.first_name, P.last_name, P.mobileno, P.email
                FROM club C INNER JOIN person P
                ON C.managed_by = P.MIS
                ORDER BY clubname'''
    parameters = None
    clubs_list = db.query(search, parameters)
    return clubs_list

def getkeys_of_place(db, place_pid):
    searchkeys =  '''SELECT kid
                     FROM killi
                     WHERE place_pid = %s'''
    parameters = (place_pid,)

    return db.query(searchkeys, parameters)


def get_accessible_placed_keys(db, person_MIS):
    search = '''SELECT DISTINCT P.name, K.kid, Q.name
                FROM place P INNER JOIN killi K INNER JOIN place Q
                ON P.pid = K.place_pid AND Q.pid = K.place_pid_store
                WHERE (K.place_pid, K.kid) IN 
                (SELECT U.key_place_pid, U.key_kid
                FROM person_memberof_club M INNER JOIN club_canuse_key U
                ON M.club_cid = U.club_cid
                WHERE %s = M.person_MIS)'''
    # search =  '''(SELECT U.key_place_pid, U.key_kid
    #             FROM person_memberof_club M INNER JOIN club_canuse_key U
    #             ON M.club_cid = U.club_cid
    #             WHERE %s = M.person_MIS)'''

    parameters = (person_MIS,)

    return db.query(search, parameters)

def get_accessible_held_keys(db, person_MIS):

    search = '''SELECT DISTINCT P.name, K.kid, Q.MIS, Q.first_name, Q.last_name, Q.mobileno, Q.email
                FROM place P INNER JOIN killi K INNER JOIN person Q
                ON P.pid = K.place_pid AND Q.MIS = K.person_MIS
                WHERE K.person_MIS <> %s
                AND (K.place_pid, K.kid) IN 
                (SELECT U.key_place_pid, U.key_kid
                FROM person_memberof_club M INNER JOIN club_canuse_key U
                ON M.club_cid = U.club_cid
                WHERE %s = M.person_MIS)'''
    # search =  '''(SELECT U.key_place_pid, U.key_kid
    #             FROM person_memberof_club M INNER JOIN club_canuse_key U
    #             ON M.club_cid = U.club_cid
    #             WHERE %s = M.person_MIS)'''

    parameters = (person_MIS, person_MIS)

    return db.query(search, parameters)


def get_keys_held(db, person_MIS):
    search = '''SELECT DISTINCT P.name, K.kid
                FROM place P INNER JOIN killi K 
                ON P.pid = K.place_pid
                WHERE K.person_MIS = %s'''
    parameters = (person_MIS,)

    return db.query(search, parameters)

def user_login(db, person_MIS):
    search = '''SELECT COUNT(*)
                FROM person
                WHERE MIS = %s'''
    parameters = (person_MIS,)

    result = db.query(search, parameters)
    exists = result[0][0] == 1
    return exists
