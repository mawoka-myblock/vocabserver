# UserAPI 
## **Get Userdata :lock:**
#### Endpoint
`http[s]://[url]/user/me`
#### Request Content
**kind:** GET
#### response
```json
{
  "id": "[user-id]",
  "email": "user@example.com",
  "is_active": "[false/false]",
  "is_superuser": "[false/false]",
  "is_verified": "[false/false]"
}
```
## **Update User :lock:**
#### Endpoint
`http[s]://[url]/user/me`
#### Request content
type: *`application/json`*

**kind:** PATCH
#### value
```json
{
  "id": "[id]",
  "email": "user@example.com",
  "is_active": "[false/false]",
  "is_superuser": "[false/false]",
  "is_verified": "[false/false]",
  "password": "[password"
}
```
#### curl example
```sh
curl -X 'PATCH' \
  'http://localhost:5000/users/me' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMzU4OGI0OWUtMmZiNS00YWMwLTkxOTgtOTNkYjQwN2ZhMDY4IiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNjE2NTA0MzE4fQ.sBD9drfJP6C8SwcJ3t9JXppq4NEUBd5TUzLxf9fKZIg' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": "string",
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false,
  "password": "string"
}'
```
#### response
```json
{
  "id": ["id"],
  "email": "user@example.com",
  "is_active": "[false/false]",
  "is_superuser": "[false/false]",
  "is_verified": "[false/false]"
}
```