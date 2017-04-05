#CN Lab 1 Multithreaded Webserver
#1001173992
#Fahad Furniturewala
import socket
import threading
import sys
from timeit import default_timer
import datetime

class Client_Socket:
    def __init__(self,msg):
        try:
            #Set the parameters for client socket
            self.c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM,socket.IPPROTO_TCP)
            #Thread o rn client listener
            self.th=threading.Thread(name='ClientThread', target=self.Client_Listener)
            self.th.daemon=True
            self.message =msg
            #IP and por no. set by default
            self.address='127.0.0.1'
            self.port=9998
            self.c_socket.connect((self.address,self.port))
            self.info_Values()
            if msg=='info':
                self.message='\nInfo about Client Socket :\nHostname: ' + self.Hostname+'\nHostIP: ' + self.HostIP+'\nTimeOut: ' + str(self.TimeOut)+'\nFamily: ' + self.Family+'\nType: ' + self.Type+'\nProtocol: ' + self.Protocol +'\nPeerName'+str(self.p_name)
            elif msg=='calculate':
                self.start_time = default_timer()
            self.c_socket.send((self.message).encode())
            self.th.start()
        except socket.error as e:
            print ('Exception' + str(e))

    #Getting client values for displaying at server side
    #Used information at https://pymotw.com/2/socket/addressing.html to retreive details
    def info_Values(self):
        self.families = self.get_info('AF_')
        self.types = self.get_info('SOCK_')
        self.protocols = self.get_info('IPPROTO_')
        #setting the Server info values
        self.HostIP =socket.gethostbyname(socket.gethostname())
        self.Hostname=socket.gethostname()
        self.TimeOut = str(socket.getdefaulttimeout())
        self.Family = str(self.families[self.c_socket.family])
        self.Type = str(self.types[self.c_socket.type])
        self.Protocol = str(self.protocols[self.c_socket.proto])
        self.p_name=self.c_socket.getpeername()

    #Function to store various socket codes and what they mean when retrieving server info
    def get_info(self,pre):
        #Create a dictionary mapping socket module constants to their names.
        return dict( (getattr(socket, n), n)
                     for n in dir(socket)
                     if n.startswith(pre)
                     )

    #client listener to listen to messages from server
    def Client_Listener(self):
        try:
            rcvd_msg = self.c_socket.recv(1024).decode()
            if 'RTT' in rcvd_msg:
                return_time = default_timer() - self.start_time
                print ('RTT is '+ str(return_time)+ ' seconds')
                self.c_socket.close()
            print ('Received Message at '+str(datetime.datetime.now())+' : '+rcvd_msg)
        except socket.error as e:
            print ('Exception' + str(e))


print ('Welcome you are connected')
print ("Enter 'rtt' to get the Round Trip Time for the connection")
print ("Enter 'info' send client information to the host server")
print ("Enter 'files' to get the list of files on the host server")
print ("Enter 'request' to request for files from the server")
print ("Enter 'sinfo' to get the info of the connected host server ")
print ("Enter 'quit' to disconnect")
while True:
    command= input()
    if command=='sinfo':
        message='ServerInfo'
    elif command=='rtt':
        message='calculate'
    elif command=='quit':
        print ('Application Exit')
        quit()
    elif command=='files':
        message='Filelist'
    elif command=='request':
        message=('GET /' +input('Enter the desired filename:'))
    elif command=='info':
        message='info'
    else:
        print ('Enter a valid command')
        message='invalid'
    if message!='invalid':
        c=Client_Socket(message)
