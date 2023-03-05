from math import sqrt
from random import randint
from utils import Enigma
#Halil
#Ibrahim
#MUT

class RSA:
    def __init__(self):
        self.PRIVATE_KEY=None
        self.PUBLIC_KEY=None

        self.primes=self.find_primes(400)[30:]
        self.setKeys()

    def generate_keys(self,p1,p2):
        """rivest shamir adelson algorithm to create public-private key pairs"""
        global PRIVATE_KEY
        global PUBLIC_KEY
        #random two prime keys choosed.bigger is better, but calculation is problemous
        p=p1#19
        q=p2#31
        
        n=p*q
        z=(p-1)*(q-1)

        #select an e that 1<e<phi(n) relatively prime with z
        #e not a factor of n phi(n)=z
        e=None
        for a in range(z-1,1,-1):
            if self.is_relatively_prime(a,z):
                e=a
                
        #choose d such that (e*d)-1 mod z == 0
        #or d=1+(k*e*z) | d=e-1 % z
        d=1
        while (e*d)%z!=1:
            d+=1

        #n,e is public key to encrypt
        #n,d is private key to decrypt
        self.PRIVATE_KEY=(n,d)
        self.PUBLIC_KEY=(n,e)

    def setKeys(self):

        r1=self.primes.pop( randint(0,len(self.primes)-1 ) )#[ randint(0, len(P_NUMS)-1 ) ]
        r2=self.primes.pop( randint(0,len(self.primes)-1 ) )#[ randint(0, len(P_NUMS)-1 ) ]
        self.generate_keys(r1,r2)#create public and private keys from prime nums
        

    @staticmethod
    def gcd(a,b):
        """find greatest common divisor between two numbers"""
        while b!=0:
            a,b=b,a%b
        return a

    @staticmethod
    def is_relatively_prime(num,num2):
        """find is these two number relatively prime.
        if gcd(num1,num2)==1->relatively prime"""
        return RSA.gcd(num,num2)==1

    #https://www.baeldung.com/cs/prime-number-algorithms
    @staticmethod
    def find_primes(r2):
        """sieve of eratosthenes to find prime numbers between range r2
        referance: https://www.baeldung.com/cs/prime-number-algorithms"""
        r1=2
        
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
#
#
#
if __name__=="__main__":
    rsa=RSA()
    #create public and private keys from prime nums

    print("public key:",rsa.PUBLIC_KEY)
    print("private key:",rsa.PRIVATE_KEY)

    message=bytearray("this is an example message to send over internet","utf-8")
    
    ciphered=Enigma.encrypt(message,rsa.PUBLIC_KEY)
    print("ciphered message with public key:", [chr(c) for c in ciphered] )
    deciphered=Enigma.decrypt(ciphered,rsa.PRIVATE_KEY)
    print("deciphered message with private key:", [chr(c) for c in deciphered]  )
