import socket
from threading import Thread
from RSA import *
from utils import *
"""Halil Ibrahim MUT"""
#
#
#
class CommunicationObject:
    def __init__(self):
        self.ip="127.0.0.1"#communication end, ip of your ethernet or wifi-card.
        self.port=65001  #listen port of ip,which port you waiting for other end
        self.rsa_keys=RSA()
        
        self.remote_ip=self.remote_ip="127.0.0.1"#to run server&client
        self.remote_port=65001                   #on same computer. 
        self.REMOTE_KEY=None

        self.init_info()
        
    def receiver(self,conn):
        while True:
            rc=conn.recv(1024) #wait for data
            data=DataManipulator.bytehex_parser( rc.hex() )#turn bytes to (8 bit each) hex list

            message=''
            while len(data)>0:
                size=int(data.pop(0) ,16)#length of first hex data(8 bit)

                string=''
                for a in range(size//2):
                    string+=data.pop(0)

                string= int(string,16)# turn encrypted hex to int
                message+= chr( Enigma.decrypt([string],self.rsa_keys.PRIVATE_KEY)[0] )
                
            print(f'{self.remote_ip}:',message )
            

            if not rc:
                print('receiver exit..')
                exit(0)
    
    def sender(self,conn):
        while True:

            data=input('Message: ')

            data=bytearray(data,"utf-8")
            data=Enigma.encrypt(data, self.REMOTE_KEY)

            #turn hex data to bytearray
            data=DataManipulator.hex_to_bytearray( DataManipulator.int_to_hex(data) )
            conn.sendall( data )


            #conn.sendall( bytearray(data, "utf-8") )

            if not data:
                print('sender exit..')
                exit(0)

    def init_info(self):
        print("Initialized")
        print("-"*40)
        print("Public Key:",self.rsa_keys.PUBLIC_KEY)
        print("Private Key:",self.rsa_keys.PRIVATE_KEY)
        print("-"*40)
    
    def handshake(self):
        pass

    def start(self):
        pass
#
#
#
if __name__=="__main__":
    pass
