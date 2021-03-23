# VocabAPI
## **Get list of vocab :lock:**
#### Endpoint
`http[s]://[url]/api/vocab/list-list`
#### response
IS BROKEN NEEDS TO BE REWRITTEN
## **Write vocab to server :lock:**
#### Endpoint
`http[s]://[url]/api/vocab/add-list/{subject}/{classroom}/{id}`
#### Request content
type: *`application/x-www-form-urlencoded`*
**kind**: POST
#### value
```json

```
#### curl example
```shell
curl -X 'POST' \
  'http://localhost:5000/api/vocab/add-list/french/003/11' \
  -H 'accept: application/json' \
  -H 'Authorization: [auth token] \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'lone=[German Wort]&ltwo=[Wort in fremdsprache]'
```
#### response
```shell
"hallo"
```
!!! info
    **The response is every time `"hallo"`**

## **Read vocab from server :lock:**
## Endpoint
`http[s]://[url]/api/vocab/read-list/{subject}/{classroom}/{id}`
#### response
```json
{
  "[German word]": "[Word in other language]",
  "[German word]": "[Word in other language]"
}
```


