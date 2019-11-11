from errors import *
from mysql.connector import errorcode

def getpeople(db):
    search = '''SELECT MIS, first_name, last_name
                FROM person
                ORDER BY MIS'''
    parameters = None
    return db.query(search, parameters)

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
    search = '''SELECT DISTINCT P.pid, P.name, K.kid, Q.name
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


def get_requested_keys(db, person_MIS):
    search = '''SELECT K.place_pid, Q.name, K.kid, 
                       P.MIS, P.first_name, P.last_name,
                       P.mobileno, P.email
                FROM place Q INNER JOIN request_key R INNER JOIN killi K INNER JOIN person P
                ON K.person_MIS = P.MIS
                AND (R.key_id, R.place_pid) = (K.kid, K.place_pid)
                AND Q.pid = R.place_pid
                WHERE R.destination = %s'''
    parameter =  (person_MIS,)

    return db.query(search, parameter)

def get_accessible_held_unrequested_keys(db, person_MIS):

    search = '''SELECT DISTINCT P.pid, P.name, K.kid, Q.MIS, Q.first_name, Q.last_name, Q.mobileno, Q.email
                FROM place P INNER JOIN killi K INNER JOIN person Q
                ON P.pid = K.place_pid AND Q.MIS = K.person_MIS
                WHERE K.person_MIS <> %s
                AND (K.place_pid, K.kid) IN 
                (SELECT U.key_place_pid, U.key_kid
                FROM person_memberof_club M INNER JOIN club_canuse_key U
                ON M.club_cid = U.club_cid
                WHERE %s = M.person_MIS)
                AND (%s, K.place_pid, K.kid) NOT IN
                (SELECT R.destination, R.place_pid, R.key_id
                FROM request_key R)'''
    # search =  '''(SELECT U.key_place_pid, U.key_kid
    #             FROM person_memberof_club M INNER JOIN club_canuse_key U
    #             ON M.club_cid = U.club_cid
    #             WHERE %s = M.person_MIS)'''

    parameters = (person_MIS, person_MIS, person_MIS)

    return db.query(search, parameters)


def get_keys_held(db, person_MIS):
    search = '''SELECT DISTINCT P.name, P.pid, K.kid
                FROM place P INNER JOIN killi K 
                ON P.pid = K.place_pid
                WHERE K.person_MIS = %s'''
    parameters = (person_MIS,)

    return db.query(search, parameters)

def get_key_requests_to_me(db, person_MIS):
    search = '''SELECT DISTINCT P.pid, P.name, K.kid, 
                Q.MIS, Q.first_name, Q.last_name,
                Q.mobileno, Q.email
                FROM place P INNER JOIN killi K INNER JOIN request_key R 
                INNER JOIN person Q
                ON P.pid = K.place_pid 
                AND (K.kid, K.place_pid) = (R.key_id, R.place_pid)
                AND R.destination = Q.MIS
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

def valid_places_for_key(db, place_pid):
    search = '''SELECT DISTINCT pid, name
                FROM place
                WHERE pid = %s OR store = true'''
    parameters = (place_pid,)

    return db.query(search, parameters)


def clubs_managed_by(db, person_MIS):
    search = '''SELECT cid, clubname
                FROM club
                WHERE managed_by = %s'''
    parameters = (person_MIS,)

    return db.query(search, parameters)


def getmembersofclubimanage(db, club_cid, my_mis):
    search = '''SELECT P.MIS, P.first_name, P.last_name,
                P.mobileno, P.email
                FROM person_memberof_club M INNER JOIN person P
                ON M.person_MIS = P.MIS
                WHERE M.club_cid = %s AND P.MIS <> %s'''
    parameters = (club_cid, my_mis)
    return db.query(search, parameters)

def get_myclubs(db, person_MIS):
    search = '''SELECT C.cid, C.clubname
                FROM club C INNER JOIN person_memberof_club M
                ON C.cid = M.club_cid
                WHERE M.person_MIS = %s'''
    parameters = (person_MIS,)
    return db.query(search, parameters)

def getallcandidates_notme(db, my_mis):
    search = '''SELECT MIS, first_name, last_name
                FROM person
                WHERE MIS <> %s'''
    parameters = (my_mis,)
    return db.query(search, parameters)

def getkeysinfo(db, place_pid):
    killisearch = '''SELECT kid
                     FROM killi
                     WHERE place_pid = %s'''
    parameters = (place_pid,)
    
    extractfirst = lambda x: x[0]

    list_of_keys = list(map(extractfirst, db.query(killisearch, parameters)))

    keys_and_permissions = []

    for key in list_of_keys:
        print(key)
        search_clubs_permitted = '''SELECT C.cid, C.clubname
                                    FROM club_canuse_key U
                                    INNER JOIN club C
                                    ON C.cid = U.club_cid
                                    WHERE (U.key_place_pid, U.key_kid) =
                                    (%s, %s)'''
        parameters = (place_pid, key)

        permitted_clubs_list = db.query(search_clubs_permitted, parameters)

        search_not_permitted_clubs ='''SELECT cid, clubname
                                       FROM club
                                       WHERE cid NOT IN
                                       (SELECT C.cid
                                       FROM club_canuse_key U
                                       INNER JOIN club C
                                       ON C.cid = U.club_cid
                                       WHERE (U.key_place_pid, U.key_kid) =
                                       (%s, %s))'''
        parameters = (place_pid, key)
        not_permitted_clubs_list = db.query(search_not_permitted_clubs, parameters)

        keys_and_permissions.append((key,
                permitted_clubs_list, 
                not_permitted_clubs_list))
    
    return keys_and_permissions


def getplacename(db, place_pid):
    search = '''SELECT name 
                FROM place
                WHERE pid = %s'''
    parameters = (place_pid,)
    extractfirst = lambda x: x[0][0]
    placename = extractfirst(db.query(search, parameters))
    return placename

