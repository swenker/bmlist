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


openshift:
ssh://5333052ae0b8cde28f00001e@bm-gjkv86.rhcloud.com/~/git/bm.git/
ssh 5333052ae0b8cde28f00001e@bm-gjkv86.rhcloud.com
swenker@126.com/

cases:
1.get a book and need to added into the databases:
  open browser and input the isbn,
  if db contains it, it will be shown to user directly.
  else system will fetch it from remote and show it to user.
        if the book was retrieved successfully
            The user can accept all the fields returned or modify some of them and then save it to db.
        else if the book wasn't found,user can add it themselves.

2.get book info by isbn

3.search book by title

4.search book by author

5.browser booklist

admin cases:
export booklist to xml?
import book from xml

delete book
update book


publish:
python pub.py local

D:\work\projects\111-tech-bmlist\bmlist>python test\test_bookparser.py

run background
cd bmlist && nohup python bmweb.py &

mysql -ubmlist -pbmlist1 -hdemodb01.qasvc.mscc.cn -Dbmlist --default-character-set=utf8 -e 'select isbn13,count(1) from bm_book group by isbn13 having count(1)>1'
mysqldump -ubmlist -pbmlist1 -hdemodb01.qasvc.mscc.cn --skip-add-drop-table --skip-extended-insert --default-character-set=utf8 bmlist>20140609.dump

git tag -a 1.0.0 -m "Initial release with data"
git push origin --tags


