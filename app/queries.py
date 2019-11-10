from errors import *
from mysql.connector import errorcode


def getplaces(db):
    
    search = '''SELECT pid, name, store
              FROM place
              ORDER BY name'''
    parameters = None
    places_list = db.query(search, parameters)
    return places_list
