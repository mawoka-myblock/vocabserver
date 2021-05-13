from config import getdatadir, getdb
from contextlib import suppress
from cloudant import CouchDB
years = ["five", "six", "seven", "eight"]

client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
print("Creating Database structure...")
with suppress(Exception):
    client.create_database("userdata", partitioned=True)
with suppress(Exception):
    client.create_database("vocab", partitioned=True)

with suppress(Exception):
    for i in years:
        print(f'Creating Database "{i}"')
        client.create_database(i, partitioned=True)



print("Done!")