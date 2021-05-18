import pywebio

import asyncio
from pywebio.session import *
from pywebio.output import *
from icecream import ic
import requests
async def main():
    response = requests.post(f'http://127.0.0.1:8000/api/v1/auth/jwt/login',
                             headers={'accept': 'application/x-www-form-urlencoded',
                                      'Content-Type': 'application/x-www-form-urlencoded'},
                             data={'grant_type': '', 'username': f'test@test.test',
                                   'password': f'testtest', 'scope': '', 'client_id': '',
                                   'client_secret': ''})
    print(response.text)

if __name__ == "__main__":
    asyncio.run(main())