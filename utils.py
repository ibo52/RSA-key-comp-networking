"""utilities to use over communication send/receive phases
halil ibrahim MUT"""

def int_to_hex(data:list):
    """turn integer list to hex string list with its hex length info before every hex.
it prepares integers to be send as hex"""
    l=[]
    for a in data:
        hex_a=hex(a).replace("0x","")# remove hex marker from string(ex: 0xff->ff)

        #make hex str mult of two(required to represent as bytes)
        while len(hex_a)%2!=0:
            hex_a="0"+hex_a

        #add length of hex before hex value
        size_info=hex(len(hex_a)).replace('0x','')
        
        while len(size_info)%2!=0:
            size_info="0"+size_info
            
        hex_a=size_info + hex_a
        
        l.append( hex_a )
        
    return l

def bytearray_from_hex(data:list):
    """turn hex array to bytearray. bytearrays can be send over internet"""
    l=bytearray()
    for a in data:
        l+=bytes.fromhex(a)
    return l

def bytehex_parser(data:str):
    """parse hex string to list of hex strings as 8-bit each"""
    l=[]
    for a in range(0,len(data),2):

        l.append( data[a:a+2] )
    return l

def hex_to_int(data:str):
    """turn hex strings to list of integers."""
    l=[]
    for a in range(0,len(data),2):

        l.append( int(data[a:a+2], 16) )
    return l

def int_to_str(data:list):
    """turn int(s) to char array(strings)"""
    string=""
    for a in data:
        string+=chr(a)
    return string

if __name__=="__main__":
    a=bytearray("deneme","utf-8")
    b=hex_to_int(a.hex())

    print("bytearray:",b,"\nstring:",int_to_str(b))

    from RSA import *
    print("public:",PUBLIC_KEY,"private:",PRIVATE_KEY)


    en=encrypt(a,PUBLIC_KEY)
    de=decrypt(en,PRIVATE_KEY)

    print("original:",int_to_str(a),b)
    print("encrypted:",int_to_str(en),en)
    print("decrypted:",int_to_str(de),de)

    print("="*40)
    print("string sdeneme hex reader ile\n")
    print("-"*40)

    en=bytehex_parser(a.hex())#hex deperlerini çıkar
    #en=bytearray_from_hex(en)
    
    en=encrypt(a,PUBLIC_KEY)#şifrele
    en=int_to_hex(en)#şifreli değeri hex string yap
    en=bytearray_from_hex(en)#hex string listesindekileri bytearraya çevir
                    #bytearrayı hex yap, inte çevir, decode et, yaz
    print(en)
    exit()
    de=decrypt(en,PRIVATE_KEY)

    print("original:",int_to_str(a),b)
    print("encrypted:",int_to_str(en),en)
    print("decrypted:",int_to_str(de),de)
    
