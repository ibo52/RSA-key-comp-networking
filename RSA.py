from math import sqrt
from random import randint
#
#
#
PRIVATE_KEY=None
PUBLIC_KEY=None

def RSA(p1,p2):
    """rivest shamir adelson algorithm to create public-private key pairs"""
    global PRIVATE_KEY
    global PUBLIC_KEY
    #random two prime keys choosed.bigger is better, but calculation is problemous
    p=p1#19
    q=p2#31
    
    n=p*q
    z=(p-1)*(q-1)

    #select an e that relatively prime with z
    e=None
    for a in range(n-1,1,-1):
        if is_relatively_prime(a,z):
            e=a
            break;

    d=1
    #choose d such that (e*d)-1 mod z == 0
    while ( (e*d)%z!=1 ):
        d+=1
        
    #n,e is public key to encrypt
    #n,d is private key to decrypt
    PRIVATE_KEY=(n,d)
    PUBLIC_KEY=(n,e)


def gcd(a,b):
    """find greatest common divisor between two numbers"""
    while b!=0:
        a,b=b,a%b
    return a

def is_relatively_prime(num,num2):
    """find is these two number relatively prime.
    if gcd(num1,num2)==1->relatively prime"""
    return gcd(num,num2)==1

#https://www.baeldung.com/cs/prime-number-algorithms
def prime_find(r2,r1=2):
    """sieve of eratosthenes to find prime numbers between range r2
    referance: https://www.baeldung.com/cs/prime-number-algorithms"""

    primes=[True for a in range(r2+1)]
    
    root_r2=sqrt(r2+1)
    for i in range(r1,int(root_r2+1)):
        if primes[i]==True:
            
            sq_i=i**2

            while sq_i<=r2:
                primes[sq_i]=False
                sq_i+=i

    x=[]
    for idx in range(r1,r2+1):
        if(primes[idx]==True):
            x.append(idx)

    return x

def encrypt(message,key:tuple):
    "message^e mod n formula ciphers the ascii message"

    ciphered=""
    for a in message:
        ciphered+= chr( ord(a)**key[1] % key[0] )
        
    return ciphered

def decrypt(message,key:tuple):
    "as c represents encrypted_message: c^d mod n formula decyphers the message by ascii table"

    deciphered=""
    for a in message:
        deciphered+= chr( ord(a)**key[1] % key[0] )
        
    return deciphered


#init-declare required vals and functions
P_NUMS=prime_find(50)
r1=P_NUMS[ randint(0, len(P_NUMS)-1 ) ]
r2=P_NUMS[ randint(0, len(P_NUMS)-1 ) ]
RSA(r1,r2)#create public and private keys from prime nums

if __name__=="__main__":
    print("choosen prime nums:",r1,r2)
    print("public key:",PUBLIC_KEY)
    print("private key:",PRIVATE_KEY)

    message="this is an example message to send over internet"
    ciphered=encrypt(message,PUBLIC_KEY)
    print("ciphered message with public key:", ciphered )
    print("deciphered message with private key:", decrypt(ciphered,PRIVATE_KEY) )
