import socket
import select
import MySQLdb
import MySQLdb.cursors
import pickle

def sendMessage(channel, msg):
   if isinstance(msg, int):
       ret = "%010d" % msg
   else:
       l = len(msg)
       ret = "%010d%s" % (l, msg)

   totalsent = 0
   msglen = len(ret)
   while totalsent < msglen:
      sent = channel.send(ret)
      totalsent += sent

print "Starting the DB server"
conn = None

serversocket = socket.socket(
 socket.AF_INET, socket.SOCK_STREAM)

running = False
try:
    serversocket.bind(('', 33066))
except:
    print "Unable to connect to socket!"
    running = False
else:
    serversocket.listen(1)
    running = True

while running:
   inputready, outputready, errorready = select.select([serversocket],
                                          [],
                                          [],
                                          2)

   for s in inputready:
       channel, details = s.accept()
       cnt = channel.recv(10)
       data = channel.recv ( int(cnt) )
       d = pickle.loads(data)
       command = d['command']
       if 'params' in d: params = d['params']
       if command == 'connect':
         if conn==None:
           print "Connecting to %s" % params['host']
           try:
               conn = MySQLdb.connect(host=params['host'],
                 user=params['user'], passwd=params['passwd'],
                 port=params['port'], db=params['db'],
                 connect_timeout=20)
           except:
               print "Failed to connect to the database"
               sendMessage(channel, 0)
           else:
               if not params['nowait']: sendMessage(channel, 1)
               print "Connected to the database"
         else:
           print "Already connected to the databse"
           sendMessage(channel, 1)

       if command == 'query':
         single = False
         if 'single' in params: single = params['single']
         cursor = conn.cursor(MySQLdb.cursors.DictCursor)
         cursor.execute(params['query'])
         if single:
             results = cursor.fetchone()
             totalcount = 1
         else:
             results = cursor.fetchall()
             totalcount = cursor.rowcount

         retval = {'totalcount': totalcount, 'results': results}
         r = pickle.dumps(retval, 2)
         sendMessage(channel, r)

       if command == 'exit':
           print "Bye Bye"
           running = False

       channel.close()

serversocket.close()
print "DB server exiting"