import sys
from inserts import *

conn = killiconnection()
if not conn:
    sys.exit(1)

"""
ret = registeruser(conn, "1145", "Ard", "inus", "8000000000", "ard@tak.com")
print(ret)
ret = registeruser(conn, "1145", "Ard", "inus", "1000000000", "ar1@tak.com")
ret = registeruser(conn, "1146", "Ard", "inus", "2000000000", "ar2@tak.com")
ret = registeruser(conn, "1147", "Ard", "inus", "3000000000", "ar3@tak.com")
ret = registeruser(conn, "1148", "Ard", "inus", "4000000000", "ar4@tak.com")
ret = registeruser(conn, "1149", "Ard", "inus", "5000000000", "ar5@tak.com")
ret = registeruser(conn, "11450", "Ard", "inus","6800000000", "ar6@tak.com")
"""




ret = addclub(conn, "CSAT")
print(ret)

