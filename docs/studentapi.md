## **Get the stats for a student :lock:**
### Endpoint
`http[s]://[url]/api/students/get-stats/{subject}`

response:




## **Write stats to server :lock:**
#### Endpoint
`http[s]://[url]/api/students/write-stats/{subject}`
#### Request content
type: *`application/x-www-form-urlencoded`*
**kind:** POST
#### value
```
ltwo: [The word for the other language]
hdiw: [How dood it worked]
```
!!! info
    **`ltwo`** stands for: **`language two`**

    **`hdiw`** stands for: **`how did it work?`**

    **`hdiw` takes a value from 0 to 3. 0 means that the student doesnt known thath word, 1 and 2 mean that the student knew the word by 2nd or 3rd try.
    3 means that the student never got the word right!**
#### response
```json
"Success"
```

## **Delete stats :lock:**
#### Endpoint
`http[s]://[url]/api/students/delete-stats/{subject}`
#### Request Content
**kind:** DELETE



