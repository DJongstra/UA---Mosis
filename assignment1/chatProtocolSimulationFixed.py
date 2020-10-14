#
#
# chatProtocolSimulation.py
#
# chat protocol (simulation) implementation (with bug(s))
#
# HV 2003, updated 2020
#

"""
"""

# Import for uniform random number generators 
from random import uniform
from random import randint

import time

class Client:
  """
  """
  
  # class attribute
  clientCount = 0
  
  def __init__(self):
    self.clientID = self.clientCount
    self.__class__.clientCount += 1
    self.connected = False
    
  def accept(self):
    self.connected = True
  
  def reject(self):
    self.connected = False
  
  def broadcast(self, message):
    pass
    
  def __str__(self):
    return "## Client " + str(self.clientID) + "'s connection status: " + str(self.connected)
    
    
class Manager:
  """
  """
  
  def __init__(self):
    self.connections = []
    
  def request(self, roomID, clientID):    
    print("## (Client %d) A connection request is sent to chat room %d." % (clientID, roomID))
    print("(CL %d) RS %d." % (clientID, roomID))
    room = g_roomMap[roomID]
    room.request(clientID)
  
  def accept(self, roomID, clientID):  
    client = g_clientMap[clientID]
    client.accept()
    self.connections.append((clientID, roomID))
    
  def reject(self, clientID):  
    client = g_clientMap[clientID]
    client.reject()
    
  def sendMessage(self, senderID, msg):        
    print("## (Client %d) Says: %s" % (senderID, msg))
    print("(CL %d) SY: %s" % (senderID, msg))
    for (clientID, roomID) in self.connections:
      if clientID == senderID:
        room = g_roomMap[roomID]
        print("## (Chat room %d) Received message from client %d: %s" % (roomID, senderID, msg))
        print("(CR %d) RM %d: %s" % (roomID, senderID, msg))
        room.sendMessage(senderID, msg)
        return
        
  def broadcast(self, roomID, senderID, msg):
    print("## (Chat room %d) Sent message to all connected clients except client %d: %s" % (roomID, senderID, msg))
    print("(CR %d) SM %d: %s" % (roomID, senderID, msg))
    for (clientID, rmID) in self.connections:
      if roomID == rmID:
        client = g_clientMap[clientID]
        if clientID != senderID:
            client.broadcast(msg)
            print("## (Client %d) Received message from client %d: %s" % (clientID, senderID, msg))
            print("(CL %d) RM %d: %s" % (clientID, senderID, msg))
        
  def __str__(self):
    return "## Connections dumping:\n" + "\n".join(["## Client %d <--> Chat room %d" % (clientID, roomID) for (clientID, roomID) in self.connections])
        
class Chatroom:
  """
  """
  
  # class attribute
  chatroomCount = 0
  clientsLimit = 4
  
  def __init__(self):
    self.roomID = self.chatroomCount
    self.__class__.chatroomCount += 1
    self.messages = []
    self.clientnum = 0
        
  def request(self, clientID):
    print("## (Chat room %d) Received connection request from client %d." % (self.roomID, clientID))
    print("(CR %d) RR %d." % (self.roomID, clientID))
    if self.clientnum < self.__class__.clientsLimit:
      self.clientnum += 1
      print("## (Chat room %d) Accepted client %d." % (self.roomID, clientID))
      print("(CR %d) AC %d." % (self.roomID, clientID))
      g_manager.accept(self.roomID, clientID)
      print("## (Client %d) Accepted by chat room %d." % (clientID, self.roomID))
      print("(CL %d) AB %d." % (clientID, self.roomID))
    else:
      print("## (Chat room %d) Rejected client %d." % (self.roomID, clientID))
      print("(CR %d) RC %d." % (self.roomID, clientID))
      g_manager.reject(clientID)
      print("## (Client %d) Rejected by chat room %d." % (clientID, self.roomID))
      print("(CL %d) RB %d." % (clientID, self.roomID))
    print(g_manager)
  
  def sendMessage(self, senderID, msg):
    self.messages.append((senderID, msg))
    g_manager.broadcast(self.roomID, senderID, msg)
    
  def __str__(self):
    return "## Chat room %d connected by %d clients has received %d messages." % (self.roomID, self.clientnum, len(self.messages))
    

# global attributes
g_clientMap = {}
g_roomMap = {}
g_manager = Manager()

def simulateChatProtocol(clientnum=6, roomnum=2):
  print("## ============= Initialization (Total: %d Clients, %d Chatrooms) =============" % (clientnum, roomnum))
  for i in range(clientnum):
    client = Client()
    g_clientMap[client.clientID] = client
    print(client)
  for i in range(roomnum):
    room = Chatroom()
    g_roomMap[room.roomID] = room
    print(room)
    
  print("## ============= Output message abbreviation =============")
  print("## CL := Client")
  print("## CR := Chat room")
  print("## RS := A connection request is sent to chat room")
  print("## RR := Received connection request from client")
  print("## AC := Accepted client")
  print("## AB := Accepted by chat room")
  print("## RC := Rejected client")
  print("## RB := Rejected by chat room")
  print("## SY := Says")
  print("## RM := Received message from client")
  print("## SM := Sent message to all connected clients except client")

  print("## ============= Running =============")

  messages = [
              "Howdy",
              "Nice to meet you!",
              "What's up?",
              "Nothing much going on ...",
              "Bla Bla Bla ..."
             ]

  numTimeSteps=50
  for time in range(numTimeSteps):
    print("## --- time = %d --------------------------------------------------------------------------" % time)
    clientID = randint(0, clientnum-1)
    roomID = randint(0, roomnum-1)
    client = g_clientMap[clientID]
    if not client.connected:
      g_manager.request(roomID, clientID)
    if client.connected:
      msg = messages[randint(0, len(messages)-1)]
      g_manager.sendMessage(clientID, msg)
    
if __name__ == "__main__":    
  simulateChatProtocol() 

   
