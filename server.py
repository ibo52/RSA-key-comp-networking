import socket
from threading import Thread
from RSA import *
from utils import *
from communicationObject import CommunicationObject
"""Halil Ibrahim MUT"""
#
#
#
class Server(CommunicationObject):

    def handshake(self,conn):
        #fitst,send your public key to other end, turn integers to bytes
        data=[x for x in self.rsa_keys.PUBLIC_KEY]
        data=DataManipulator.hex_to_bytearray( DataManipulator.int_to_hex(data) )

        conn.sendall( data )#send


        #second, wait for other end to send its key
        p1=conn.recv(1024)

        data= DataManipulator.bytehex_parser(p1.hex())
        CLI_KEY=[]
        while len(data)>0:
                size=int(data.pop(0) ,16)#length of first hex data(8 bit)

                string=''
                for a in range(size//2):
                    string+=data.pop(0)

                string= int(string,16)# turn encrypted hex to int
                CLI_KEY.append(string)

        return tuple( CLI_KEY )

    def start(self):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            print("setting main server..")
            try:
                s.bind((self.ip,self.port))
            except OSError as e:
                print("\nPossibly threads running on backround. Close from sys-monitor")
                exit(e)

            print('server setted. Listening..')
            s.listen()

            conn,addr=s.accept()
            self.remote_ip,self.remote_port=addr

            with conn:
                print(f'client connected. ip,addr:{addr}')

                CLI_KEY=self.handshake(conn)
                print("public key reached:",CLI_KEY)
                self.REMOTE_KEY=CLI_KEY
                print("="*40)

                #send - receive (thread)
                threads=[ Thread(target=self.receiver,args=(conn,) ),
                  Thread(target=self.sender,args=(conn,) )
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
    server=Server()
    server.start()
