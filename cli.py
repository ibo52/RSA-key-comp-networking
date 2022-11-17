import socket
from threading import Thread
from RSA import *
from utils import *
"""Halil Ibrahim MUT"""

server="127.0.0.1"#communication end, ip of those who you want to communicate
port=65001      #listen port of ip,which port it is waiting for you

def receiver(conn,addr):
    while True:
        rc=conn.recv(1024) #wait for data
        data=bytehex_parser( rc.hex() )#turn bytes to (8 bit each) hex list

        message=''
        while len(data)>0:
            size=int(data.pop(0) ,16)#length of first hex data(8 bit)

            string=''
            for a in range(size//2):
                string+=data.pop(0)

            string= int(string,16)# turn encrypted hex to int
            message+= chr( decrypt([string],PRIVATE_KEY)[0] )

        print(f'{addr}:',message )
        

        if not rc:
            print('receiver exit..')
            exit(0)
    
def sender(conn, SRV_KEY):
    while True:
        data=input('Message: ')
        data=bytearray(data,"utf-8")
        data=encrypt(data,SRV_KEY)

        #turn hex data to bytearray
        data=bytearray_from_hex( int_to_hex(data) )
        conn.sendall( data )
        
        
        #conn.sendall( bytearray(data, "utf-8") )

        if not data:
            print('sender exit..')
            exit(0)

def cli_handshake(conn):

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
    data=[x for x in PUBLIC_KEY]
    data=bytearray_from_hex( int_to_hex(data) )
    
    conn.sendall( data )#send
    
    return tuple( SRV_KEY )

def init_info(text="CLIENT\n"):
    print(text,"-"*40)
    print(f"PUBLIC:{PUBLIC_KEY}\nPRIVATE:{PRIVATE_KEY}")
    print("-"*40)
    
if __name__=='__main__':
    init_info()
    
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        print('trying to connect main server..',end="")
        try:
            s.connect( (server,port) )
        except Error as e:
            print(e,"\nreturned")
            exit(e)
            
        print("SUCCESS")

        """
        #wait for servers public key
        p1=s.recv(1024)
        p2=s.recv(1024)

        #interpret incoming bytes as integer
        SRV_KEY=(int.from_bytes(p1,"big"), int.from_bytes(p2,"big") )
        print("public key reached:",SRV_KEY)

        #send your key int.to_bytes(bytes=1,byteorder=little/big endian)

        #turn integers to bytes
        s.sendall( (PUBLIC_KEY[0]).to_bytes(2,"big") )
        s.sendall( (PUBLIC_KEY[1]).to_bytes(2,"big") )
        """
        SRV_KEY=cli_handshake(s)
        print("public key reached:",SRV_KEY)
        print("="*40)
        
        
        #send - receive (thread)
        threads=[ Thread(target=receiver,args=(s,server,) ),
              Thread(target=sender,args=(s, SRV_KEY,) )
            ]
        for thr in threads:
            thr.daemon=True
            thr.start()
            
        for thr in threads:
                thr.join()
    
    print('EXIT')
