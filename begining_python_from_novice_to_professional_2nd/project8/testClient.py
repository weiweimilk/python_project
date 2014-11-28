
from xmlrpclib import *

mypeer = ServerProxy('http://localhost:4242')
mypeer.hello('http://localhost:4243')


code, data = mypeer.query('test.txt')
print code
print data

mypeer.fetch('test.txt', 'secret1')
