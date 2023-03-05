import socket
from threading import Thread
from RSA import *
from utils import *
from communicationObject import CommunicationObject
"""Halil Ibrahim MUT"""
#
#
#
class Client(CommunicationObject):

    def handshake(self,conn):

        #first,receive other end's key
        p1=conn.recv(1024)

        data=bytehex_parser(p1.hex())
        SRV_KEY=[]
        while len(data)>0:
                size=int(data.pop(0) ,16)#length of first hex data(8 bit)

                string=''
                for a in range(size//2):
                    string+=data.pop(0)

                string= int(string,16)# turn encrypted hex to int
                SRV_KEY.append(string)

        #second, send your public key to other end, turn integers to bytes
        data=[x for x in self.rsa_keys.PUBLIC_KEY]
        data=bytearray_from_hex( int_to_hex(data) )

        conn.sendall( data )#send

        return tuple( SRV_KEY )

    def start(self):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            print('trying to connect main server..',end="")
            try:
                s.connect( (self.remote_ip,self.remote_port) )
            except Exception as e:
                print("\nException:",e)
                exit(e)
                
            print("[SUCCESS]:Connection established")

            SRV_KEY=self.handshake(s)
            print("public key reached:",SRV_KEY)
            self.REMOTE_KEY=SRV_KEY
            print("="*40)

            #send - receive (thread)
            threads=[ Thread(target=self.receiver,args=(s,) ),
                  Thread(target=self.sender,args=(s,) )
                ]
            for thr in threads:
                thr.daemon=True
                thr.start()
                
            for thr in threads:
                    thr.join()
#
#
#   
if __name__=='__main__':
    client=Client()
    client.start()

