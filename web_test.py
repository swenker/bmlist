
from httplib import HTTPConnection
import urllib


connection = HTTPConnection('s002.blurdev.com')

# connection.request('GET', '/books/')

data = urllib.urlencode({'login_id':'abc@tt.com','passwd':'abcd1234'})
connection.request(method='POST', url='/users/api/signin', body=data)

http_response = connection.getresponse()

response_body = http_response.read()

connection.close()

