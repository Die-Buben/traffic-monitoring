import socket
import time
#import uiConnection

host = "127.0.0.1"
port= 25001
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
isRunning = True
cartype = 'car'
          
def SendNew():
    sock.sendall(cartype.encode("UTF-8")) #Converting string to Byte, and sending it to C#
  


while isRunning:
    time.sleep(0.5) #sleep 0.5 sec
            #startPos +=1 #increase x by one
    SendNew()

    receivedData = sock.recv(1024).decode("UTF-8") #receiveing data in Byte fron C#, and converting it to String
    #print(receivedData)
    if(receivedData == 'end'):
        isRunning = False
    elif(receivedData == 'car'):
        cartype = 'car'
    elif (receivedData == 'lkw'):
        cartype = 'lkw'       