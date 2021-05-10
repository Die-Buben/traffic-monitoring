#Python multithreading example.
#1. Calculate factorial using recursion.
#2. Call factorial function using thread. 

from _thread import start_new_thread
from time import sleep
import time

threadId = 1 # thread counter

class DataHandler:
     
   def __init__(self):
      self.count = 0
      self.countadd = 1
      self.running = True

   def somehardtask(self, maxcount):
      while(self.running):
         time.sleep(1) #sleep 0.5 sec   
         self.count+=self.countadd

class Webserver:
   
   def __init__(self):
      self.count = 0
      self.counter = 0
      self.running = True

   def somehardtask(self, maxcount):
      while(self.running):
         time.sleep(3) #sleep 0.5 sec
         self.count += 1
   
   def NewCarFound(self, countall):
      print(countall)

datahandler = DataHandler()
webserver = Webserver()
start_new_thread(datahandler.somehardtask, (10,))
start_new_thread(webserver.somehardtask, (10,))

carcount = 0
carplus = 0
print("Waiting for threads to return...")
while(True):
   if(carcount != datahandler.count):
      carcount = datahandler.count
      webserver.NewCarFound(carcount)
   
   if(carplus != webserver.count):
      carplus = webserver.count
      datahandler.countadd = carplus

