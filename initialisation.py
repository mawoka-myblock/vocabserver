import sentry_sdk
sentry_sdk.init(environment="development")
sentry_sdk.init(
    "https://f09f3900a5304b768554e3e5cab68bcd@o661934.ingest.sentry.io/5764925",
    traces_sample_rate=1.0
)
from config import getdatadir, getdb
from contextlib import suppress
from cloudant import CouchDB
years = ["five", "six", "seven", "eight"]

def init(no_log):
    if not no_log:
        print("INIT PROCESS")
    client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
    #print("Creating Database structure...")
    with suppress(Exception):
        client.create_database("userdata", partitioned=True)
    with suppress(Exception):
        client.create_database("vocab", partitioned=True)
    with suppress(Exception):
        client.create_database("_users", partitioned=True)

    with suppress(Exception):
        for i in years:
            #print(f'Creating Database "{i}"')
            client.create_database(i, partitioned=True)



