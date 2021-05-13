import os

from config import getdatadir, getdb
from contextlib import suppress
from cloudant import CouchDB

client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
print("Creating Database structure...")
with suppress(Exception):
    client.create_database("userdata", partitioned=True)
with suppress(Exception):
    client.create_database("vocab", partitioned=True)

print("Done!")