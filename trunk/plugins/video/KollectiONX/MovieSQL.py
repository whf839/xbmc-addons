import SQL
import socket
import pickle
import xbmc
import time

__author__="brian"
__date__ ="$Feb 28, 2010 12:57:44 AM$"

if __name__ == "__main__":
    print "Hello World"


class MovieSQL:
    def __init__(self, dp=None, settings=None):
        self.connection = None
        self.connected = False
        self.dp = None
        self.settings = settings

    def __progressCreate(self, title):
      if self.dp != None: self.dp.create(title)

    def __progressUpdate(self, value, label1='', label2='', label3=''):
      if self.dp != None: self.dp.update(value, label1, label2, label3)

    def __progressClose(self):
      if self.dp != None: self.dp.close()

    def connect(self, host=None, port=0, user=None, passwd=None, db=None, nowait=0):
      s = socket.socket(socket.AF_INET,
                        socket.SOCK_STREAM)
      connected = False
      trycount = 0
      while not connected:
          trycount += 1
          if trycount == 5:
              print "Giving up on the dbserver"
              return -1
          try:
              s.connect(('localhost', 33066))
          except:
              print "Attempting to start the db server"
              xbmc.executescript('special://home/plugins/video/KollectiONX/DBServer.py')
              time.sleep(1)
          else:
              print "Connected to the db server"
              connected = True

      z = {'command': 'connect',
           'params': {
                      'host': host,
                      'user': user,
                      'passwd': passwd,
                      'port': port,
                      'db': db,
                      'nowait': nowait}}

      p = pickle.dumps(z,2)
      s.send("%010d%s" % (len(p), p))
      if nowait:
          print "Not waiting for results"
          self.connected = False
      else:
          results = s.recv(10)
          print "Got result %s" % results
          if int(results) == 0:
              self.connected = False
          else:
              self.connected = True

      s.close()
      return self.connected

    def lcaseRow(self, row):
        fixed = {}
        for k in row:
            fixed[k.lower()] = row[k]
            if k.lower() != k: fixed[k] = row[k]
        return fixed

    def lcaseResults(self, results):
        if isinstance(results, list) or isinstance(results, tuple):
          fixed = []
          for r in results:
            f = self.lcaseRow(r)
            fixed.append(f)
        else:
          fixed = self.lcaseRow(results)

        return fixed

    def runSQL(self, sql=None, single=False):
        s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)

        s.connect(('localhost', 33066))

        z = {'command': 'query',
             'params': {'query': sql,
                        'single': single}}
        p = pickle.dumps(z,2)
        s.send("%010d%s" % (len(p), p))
        l = int(s.recv(10))

        msg = ''
        while len(msg) < l:
            chunk = s.recv(l - len(msg))
            msg += chunk

        z = pickle.loads(msg)
        return self.lcaseResults(z['results']), z['totalcount']

    def getYearList(self):
        return self.runSQL(SQL.YEAR_LIST)

    def getGenreList(self):
        return self.runSQL(SQL.GENRE_LIST)

    def getActorLetterList(self):
        return self.runSQL(SQL.ACTOR_LETTER_LIST)

    def getActorsByLetter(self, letter):
        return self.runSQL(SQL.ACTORS_LIST % letter)

    def getActorsByMovie(self, movieid):
        return self.runSQL(SQL.ACTORS % movieid)

    def getGenresByMovie(self, movieid):
        return self.runSQL(SQL.GENRE % movieid)

    def getDirectorsByMovie(self, movieid):
        return self.runSQL(SQL.DIRECTOR % movieid)

    def getWritersByMovie(self, movieid):
        return self.runSQL(SQL.WRITER % movieid)

    def getStudiosByMovie(self, movieid):
        return self.runSQL(SQL.STUDIO % movieid)

    def getStudioList(self):
        return self.runSQL(SQL.STUDIO_LIST)
    
    def getDirectorList(self):
        return self.runSQL(SQL.DIRECTOR_LIST)

    def getWriterList(self):
        return self.runSQL(SQL.WRITER_LIST)

    def isConnected(self):
        return self.connected


