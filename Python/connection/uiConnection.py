import socket
import time

host = "127.0.0.1"
port= 25001
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
isRunning = True
cartype = 'car'
          
def SendNew(self):
    sock.sendall(cartype.encode("UTF-8")) #Converting string to Byte, and sending it to C#
  
