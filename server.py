import socket
from threading import Thread
from RSA import *
from utils import *
"""Halil Ibrahim MUT"""

server="127.0.0.1"#communication end, ip of your ethernet or wifi-card.
port=65001      #listen port of ip,which port you waiting for other end

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

def srv_handshake(conn):
    #fitst,send your public key to other end, turn integers to bytes
    data=[x for x in PUBLIC_KEY]
    data=bytearray_from_hex( int_to_hex(data) )
    
    conn.sendall( data )#send


    #second, wait for other end to send its key
    p1=conn.recv(1024)
    
    data=bytehex_parser(p1.hex())
    CLI_KEY=[]
    while len(data)>0:
            size=int(data.pop(0) ,16)#length of first hex data(8 bit)

            string=''
            for a in range(size//2):
                string+=data.pop(0)

            string= int(string,16)# turn encrypted hex to int
            CLI_KEY.append(string)

    return tuple( CLI_KEY )
    
def init_info(text="SERVER\n"):
    print(text,"-"*40)
    print(f"PUBLIC:{PUBLIC_KEY}\nPRIVATE:{PRIVATE_KEY}")
    print("-"*40)
    
if __name__=='__main__':
    init_info()
    
    #af inet==ipv4
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        print("setting main server..")
        try:
            s.bind((server,port))
        except OSError as e:
            print("\nPossibly threads running on backround. Close from sys-monitor")
            exit(e)

        print('setted. Listening..')
        s.listen()

        conn,addr=s.accept()

        with conn:
            print(f'client connected. ip,addr:{addr}')

            """
            #send your public key, turn integers to bytes
            conn.sendall( (PUBLIC_KEY[0]).to_bytes(2,"big") )
            conn.sendall( (PUBLIC_KEY[1]).to_bytes(2,"big") )
        
            #wait for other to send its key
            p1=conn.recv(1024)
            p2=conn.recv(1024)

            #interpret incoming bytes as integer
            CLI_KEY=(int.from_bytes(p1,"big"), int.from_bytes(p2,"big") )
            """
            CLI_KEY=srv_handshake(conn)
            print("public key reached:",CLI_KEY)
            print("="*40)

            #send - receive (thread)
            threads=[ Thread(target=receiver,args=(conn,server,) ),
              Thread(target=sender,args=(conn,CLI_KEY,) )
            ]
            for thr in threads:
                thr.daemon=True
                thr.start()
                
            for thr in threads:
                thr.join()
    
print('EXIT')
