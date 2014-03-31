bmlist
======
book list management

service:

GET /bm/book/list/{u}?p=0,1,2,3
GET /bm/book/get/{bid}?uid=1   [if uid is given,will also show userinfo?]

POST /bm/book/create
POST /bm/book/delete?bid= [need to check privileges,only admin can do this]
POST /bm/book/delete?bid= &uid=
POST /bm/book/add?uid=1&bid=23



