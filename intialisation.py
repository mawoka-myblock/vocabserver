import os

from config import getdatadir
from contextlib import suppress


print("Creating Database structure...")
with suppress(Exception):
    os.mkdir(getdatadir())
with suppress(Exception):
    os.mkdir(f"{getdatadir()}/userdata")
with suppress(Exception):
    os.mkdir(f"{getdatadir()}/vocab")

print("Done!")