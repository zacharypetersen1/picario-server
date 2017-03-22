'''
The MIT License (MIT)
Copyright (c) 2013 Dave P.
'''

import json
import signal
import sys
import ssl
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer
from optparse import OptionParser
from PicarioServer import *


# data structures for managing clients
maxPlayers = 64
openIds = []
clients = {}

#starts up PicarioServer
onStart()

# setup data structures for managing clients
for i in range(1, maxPlayers + 1):
   openIds.append(i)
   clients[i] = None

#checks if a player can join the game
def canJoin():
   if len(openIds) == 0:
       return False
   else:
       return True

#sends a message denying access to server
def refuseConnection(socket):
   msg = {"type":"error", "message":"Game full, unable to connect"}
   socket.sendMessage(json.dumps(msg))
   socket.close()

#accepts a connection and stores client in a dict
def acceptConnection(socket):
    thisID = openIds.pop(0)
    clients[thisID] = socket
    socket.myId = thisID
    outBound = onConnect(thisID)
    sendOutbound(outBound)
    msg = {"type":"connect", "id": thisID}
    socket.sendMessage(json.dumps(msg))
    print("Accepted Connection with id: " + str(thisID))

# handles client socket organization when client disconnects
def disconnect(socket):
   if(socket.myId != 0):
      clients[socket.myId] = None
      openIds.append(socket.myId)
      sendOutbound(onDisconnect(socket.myId))

# prints out the state of client sockets within server
def debugClients():
   clientsDebugStr = "{ "
   for key in clients:
      clientsDebugStr += str(key) + (":None " if clients[key] == None else ":Sock ")
   clientsDebugStr += "}"

   print("Clients  : " + clientsDebugStr)
   print("Open Ids : " + str(openIds))

def sendOutbound(outBound):
   for key in outBound:
      if (outBound[key] != None):
         for msg in outBound[key]:
            if clients[key] != None:
                clients[key].sendMessage(json.dumps(msg))
   clearMessages()

class Socket(WebSocket):

   myId = 0

   def handleMessage(self):
      message = json.loads(self.data)
      if message['type'] == 'obj':
         sendOutbound(onMessage(self.myId, message))

   def handleConnected(self):
      if(canJoin()):
         acceptConnection(self)
      else:
         refuseConnection(self)

   def handleClose(self):
      disconnect(self)


if __name__ == "__main__":

   parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
   parser.add_option("--host", default='', type='string', action="store", dest="host", help="hostname (localhost)")
   parser.add_option("--port", default=8000, type='int', action="store", dest="port", help="port (8000)")
   parser.add_option("--ssl", default=0, type='int', action="store", dest="ssl", help="ssl (1: on, 0: off (default))")
   parser.add_option("--cert", default='./cert.pem', type='string', action="store", dest="cert", help="cert (./cert.pem)")
   parser.add_option("--ver", default=ssl.PROTOCOL_TLSv1, type=int, action="store", dest="ver", help="ssl version")

   (options, args) = parser.parse_args()

   cls = Socket

   if options.ssl == 1:
      server = SimpleSSLWebSocketServer(options.host, options.port, cls, options.cert, options.cert, version=options.ver)
   else:
      server = SimpleWebSocketServer(options.host, options.port, cls)

   def close_sig_handler(signal, frame):
      server.close()
      sys.exit()

   signal.signal(signal.SIGINT, close_sig_handler)

   server.serveforever()
