from config import sentry
sentry()
from config import getdb
from contextlib import suppress
from cloudant import CouchDB
years = ["five", "six", "seven", "eight"]

def init(no_log):
    if not no_log:
        print("INIT PROCESS")
    client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
    #print("Creating Database structure...")
    client.create_database("userdata", partitioned=True)
    client.create_database("vocab", partitioned=True)
    client.create_database("sli", partitioned=True) # sli = stay_logged_in

    with suppress(Exception):
        for i in years:
            #print(f'Creating Database "{i}"')
            client.create_database(i, partitioned=True)



