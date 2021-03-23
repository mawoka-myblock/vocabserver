# AuthAPI
## **Login**
#### Endpoint
`http[s]://[url]/auth/jwt/login`

!!! info
    **requires authentification is marked with :lock:**
#### Request Content
type: *`application/x-www-form-urlencoded`*

**kind:** POST

username : *obviously the username*

password: *obviously the password*
#### curl example
```sh
  curl -X 'POST' \
  'http://localhost:5000/auth/jwt/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=[username]&password=[password]&scope=&client_id=&client_secret='
```
####  response
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMzU4OGI0OWUtMmZiNS00YWMwLTkxOTgtOTNkYjQwN2ZhMDY4IiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNjE2NDQzMDY2fQ.cUnbJq5aK1_fZtndeQf4PTwTHySfIH3lJsTiYaOhde8",
  "token_type": "bearer"
}
```
## **Register**
#### Endpoint
`http[s]://[url]/auth/register`
#### Request Content
type: *`application/json`*
**kind:** POST
#### value
```json
{
  "email": "user@example.com",
  "password": "string",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```
!!! info
    it is useless to set `"is_verified": true because it doesnt help!`
#### curl example
```sh
curl -X 'POST' \
  'http://localhost:5000/auth/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "user@example.com",
  "password": "string",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}'
```
#### response
```json
{
  "id": "354b3ffb-12ae-43e2-9728-0f454828e8ee",
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```
## **Forgot Password**
####Endpoint
`http[s]://[url]/auth/forgot-password`
####Request Content
type: *`application/json`*
**kind:** POST
###value
```json
{
  "email": "user@example.com"
}
```
#### curl example
```sh
curl -X 'POST' \
  'http://localhost:5000/auth/forgot-password' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "user@example.com"
}'
```
#### respone
**ONLY IN CONSOLE FOR NOW**
## **Forgot Password**
#### Endpoint
