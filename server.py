#CN Lab 1 Multithreaded Webserver
#1001173992
#Fahad Furniturewala
import socket
import threading
import sys
import datetime
import os

class Server_Socket:
    def __init__(self):
        try:
            #Set parameters for the server socket and start the server socket
            #IP and port values are defined here
            self.address= '127.0.0.1'
            self.port=9998
            self.s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM,socket.IPPROTO_TCP)
            self.s_socket.bind((self.address,self.port))
            self.s_socket.listen(5)
            #Running the server listener on a thread for multiple clients to be connected
            self.th = threading.Thread(name='ServerThread', target=self.Server_Listener)
            self.th.daemon=True # this is set to true so that when client quits the thread also quits
            self.th.start()
            self.info_Values()
            #initial client info value set to a default value
            self.client_info='Client information not available'
            #List containing File names available on server for the client
            self.files=['index.html','sample.txt']
        except socket.error as e:
            self.s_socket.close()
            print ('Could not open socket: ' + str(e))
            quit()

    #Getting client values for displaying at client side
    def info_Values(self):
        #Loading families,types,constants so that we can retrieve server info
        self.families = self.get_info('AF_')
        self.types = self.get_info('SOCK_')
        self.protocols = self.get_info('IPPROTO_')
        self.HostIP =socket.gethostbyname(socket.gethostname())
        self.Hostname =socket.gethostname()
        self.TimeOut = str(socket.getdefaulttimeout())
        self.Family = str(self.families[self.s_socket.family])
        self.Type = str(self.types[self.s_socket.type])
        self.Protocol = str(self.protocols[self.s_socket.proto])

    #Function to store various socket codes and what they mean when retrieving server info
    def get_info(self,pre_info):
        #Create a dictionary mapping socket module constants to their names.
        return dict( (getattr(socket, n), n)
                     for n in dir(socket)
                     if n.startswith(pre_info)
                     )

    #server Listener function that runs in a thread accepting requests from multiple clients continuously
    def Server_Listener(self):
        while 1:
            print ('Server is Waiting for a command:')
            (c_socket, address) = self.s_socket.accept()
            #storing the Peername
            p_name = c_socket.getpeername()
            try:
                rcvd_msg = c_socket.recv(1024).decode()
                #Actions to take based on message received from client and send a message back
                if rcvd_msg=='calculate':
                    c_socket.send(('RTT').encode())
                elif 'GET' in rcvd_msg: #works for when a Client OR a Browser Window requests using a get message
                    f_name=rcvd_msg.split(' /')[1].split(' ')[0]# eg GET /filename.extension
                    if f_name in self.files: #if f_name is present on server
                        current_directory = os.getcwd()
                        f = open(current_directory+"/"+f_name.strip()).read()
                        c_socket.send(('HTTP/1.1 200 OK\nContent-Type: text/html\n\n'+f).encode())
                    else:
                       c_socket.send("HTTP/1.0 404 Not Found\r\n"+"Content-type: text/html\r\n\r\n"+"<html><head></head><body>"+f_name+" not found</body></html>\n").encode()
                elif rcvd_msg=='Filelist':
                    #send list of available files on the server
                    c_socket.send((self.files[0]+','+self.files[1]).encode())
                elif rcvd_msg=='ServerInfo':
                    c_socket.send(('\nInfo about Server Socket :\nHostname: ' + self.Hostname+'\nHostIP: ' + self.HostIP+
                    '\nTimeOut: ' + str(self.TimeOut)+'\nFamily: ' + self.Family+
                    '\nType: ' + self.Type+'\nProtocol: ' + self.Protocol +'\nPeerName'+str(p_name)).encode())
                elif 'Info about Client' in rcvd_msg:
                    self.client_info=rcvd_msg;
                    c_socket.send(('Info received').encode())
                #printing the details of the client connected to server
                print('Connection parameters of connected Client ' + address[0] + ':' + str(address[1]))
                #printing messgae received from client
                print ('Received Message at '+str(datetime.datetime.now())+' : '+rcvd_msg)
                #print ('rcvd_msg: '+rcvd_msg)
                c_socket.close()
            except socket.error as e:
                print ('Socket Exception' + str(e))
                c_socket.close()
            except IOError as e:
                c_socket.send("HTTP/1.0 404 Not Found\r\n"+"Content-type: text/html\r\n\r\n"+"<html><head></head><body>"+f_name+" not found</body></html>\n")
                print ('I/O error({0}): {1}'.format(e.errno, e.strerror))
                c_socket.close()
            except:
                print ("Unexpected error:", sys.exc_info()[0])
                c_socket.close()


print ("Enter 'info' for connected client information")
print ("Enter 'quit' to disconnect")
s =Server_Socket()
while True:
    command= input()
    if command=='quit':
        print ('Application Exit')
        s.s_socket.close()
        quit()
    elif command=='info':
 	   print (s.client_info)

