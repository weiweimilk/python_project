
from xmlrpclib import ServerProxy, Fault
from os.path import join, abspath, isfile
from SimpleXMLRPCServer import SimpleXMLRPCServer
from urlparse import urlparse
import sys

SimpleXMLRPCServer.allow_reuse_address = 1

MAX_HISTORY_LENGTH = 6

UNHANDLED       = 100
ACCESS_DENIED   = 200

class UnhandleQuery(Fault):
    """
      exception: can not query
    """
    def __init__(self, message="Couldn't handle the query"):
        Fault.__init__(self, UNHANDLED, message)

class AccessDenied(Fault):
    """
      exception: no autherity
    """
    def __init__(self, message="Access denied"):
        Fault.__init__(self, ACCESS_DENIED)

def inside(dir, name):
    """
      check if the name is in dir or not
    """
    dir = abspath(dir)
    name = abspath(name)
    return name.startswith(join(dir, ''))

def getPort(url):
    """
      get port from url
    """
    name = urlparse(url)[1]
    parts = name.split(':')
    return int(parts[-1])

class Node:
    """
      p2p network
    """
    def __init__(self, url, dirname, secret):
        self.url = url
        self.dirname = dirname
        self.secret = secret
        self.known = set()

    def query(self, query, history=[]):
        """
          query file, and may get help from other nodes
          return string of file
        """
        try:
            return self._handle(query)
        except UnhandleQuery:
            history = history + [self.url]
            if len(history) >= MAX_HSITORY_LENGTH: raise
            return self._broadcast(query, history)
        
    def hello(self, other):
        """
         introduce itself to other nodes
        """
        self.known.add(other)
        return 0

    def fetch(self, query, secret):
        """
          get file 
        """
        if secret != self.secret: raise AccessDenied
        result = self.query(query)
        f = open(join(self.dirname, query), 'w')
        f.write(result)
        f.close()
        return 0

    def _start(self):
        """
          to start the XML-RPC server
        """

        s = SimpleXMLRPCServer("", getPort(self.url)), logRequests=False)
        s.register_instance(self)
        s.serve_forever()

    def _handle(self, query):
        """
          to handle query request
        """
        dir = self.dirname
        name = join(dir, query)
        if not isfile(name): raise UnhandleQuery
        if not isside(dir, name): raise AccessDenied
        return open(name).read()

    def _broadcast(self, query, history):
        """
          to broadcast the query to the adjacent nodes
        """
        for other in self.known.copy():
            if other in history: continue
            try:
                s = ServerProxy(other)
                return s.query(query, history)
            except Fault, f:
                if f.faultCode == UNHANDLED: pass
                else: self.known.remove(other)
            except:
                self.known.remove(other)
        raise UnhandledQuery

def main():
    url, directory, secret = sys.argv[1:]
    n = Node(url, directory, secret)
    n._start()

if __name__ == '__main__': main()
