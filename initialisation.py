from config import sentry

sentry()
from config import getdb, get_db_name, get_db_connection_str
from contextlib import suppress
from pymongo import MongoClient

years = ["five", "six", "seven", "eight"]


def init(no_log: bool) -> None:
    """if not no_log:
        print("INIT PROCESS")
    client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
    # print("Creating Database structure...")
    client.create_database("userdata", partitioned=True)
    client.create_database("vocab", partitioned=True)
    client.create_database("sli", partitioned=True)  # sli = stay_logged_in

    with suppress(Exception):
        for i in years:
            # print(f'Creating Database "{i}"')
            client.create_database(i, partitioned=True)"""



