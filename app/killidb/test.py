from config import *
from modifications import *
from errors import *
from database import database

def debugexec(func, *args, correctret = 0):
    ret = func(db, *args)
    if ret != 0:
        print(*args)
        print(ret)

db = database(KILLIDBCONFIG)
debugexec(registeruser, "11450", "Evil", "Mind", "1111111111", "gru@evil.com")
debugexec(registeruser, "11145", "Obidient", "Follower", "0000000000", "follow@yahoo.com")
debugexec(registerplace, "Rapid Prototyping Lab")
debugexec(registeruser, "111703333", "Yahska", "Rahdoed", "6666666666", "fighterdhingra@yahoo.com")
debugexec(registerclub, "D&D", "111703333")
debugexec(registerplace, "Boat Club Gallery")
debugexec(changemanager, "1", "11145")
debugexec(registerplace, "Security Section", True)
debugexec(addkey, 2)
debugexec(grantkeypermission, 1, 2, 1)
debugexec(addkey, 2)
debugexec(grantkeypermission, 1, 2, 1)
debugexec(addkey, 1)
debugexec(grantkeypermission, 1, 2, 2)
debugexec(addclubmember, 1, "11450")
debugexec(addclubmember, 1, "11145")
debugexec(pickup_key, "111703333", 2, 1)
debugexec(person_canuse_key, "111703333", 2, 1)
debugexec(person_canuse_key, "11145", 1, 1)
debugexec(place_key, "111703333", 2, 1, 2)
debugexec(place_key, "111703333", 2, 1, 3)
debugexec(pickup_key, "111703333", 2, 1)
#debugexec(place_key, "111703333", 2, 1, 1)
#debugexec(request_key, "11145", 2, 2)
debugexec(request_key, "11145", 2, 1)
debugexec(transfer_key, "11450", 2, 1)
debugexec(transfer_key, "11145", 2, 1)

