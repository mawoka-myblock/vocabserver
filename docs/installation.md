## Install requirements
1. `virtualenv venv`
2. `source venv/bin/activate`
!!! info
    If you are using windows:

    `source venv/bin/activate.ps`?


3. `pip3 install -r requirements.txt`
## Edit the config file
```
#config.ini

[directories]
data=/home/server/data

[server]
port=80
```
## Start the server
`uwicorn main:app --reload`
