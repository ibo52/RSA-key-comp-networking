# RSS algorithm implementation to create public-private key pairs
## note from advanced computer networks lecture
### references: powerpoint slides(ch:8, pg:21-29) of 'computer networking: a top down approach' 
***
## To provide more secure way of communication over internet;
- public keys are accessible by everyone on the internet that wants to communicate with owner of that key
- client requests public key and encrypts its symetric key with this public key, then sends to other end.
- only and only owner can decrypt this message by its private key(as long as anyone do not obtain the private key).
- owner sends a message with received symetric key.
- now they provide some secure way to communicate

## Rivet-Shamir-Adelson algorithm:
  1. select two random prime numbers: p and q(bigger is better on encrypting)
  2. let n=p*q, z=(p-1)*(q-1)
  3. choose a value e such that e is relatively prime with z --> gcd(e,z)=1
  4. choose a value d such that (e*d) mod z ==1
  5. (n,d) is private key; (n,e) is public key

## working principle of RSA:
  * Any type of property on computer science perspective, is represents as sequences of bits, So a message is also a sequence of bits(thus represents as numeric values).
  * any message encrypts as f(m)= (m^e mod n) =c
  * any ciphered message decrypts as f(c)= (c^d mod n)= m
  * we know f(m)=c so,we write an equation such as f( f(m) )=m
  * by modular arithmetic rule: (a^b mod k)^c <==> a^bc mod k <==> (a^c mod k)^b mod k
  * This rule means, its not important which function you use first. The result will be remain same. This is a very useful property.
  * so, f( f(m) ) =(m^e mod n)^d mod n == m^ed mod n.

## a simple client-server programs to communicate over internet securely by RSA
  * run on terminal : `python3 server.py`
  * run on terminal2: `python3 cli.py`
  * Send and receive messages between server and client.
  * NOTE: Only use ascii characters for now. Other characters cause undesired/broken behavior of program.
  * [x] ISSUE: Sending and receiving public keys sometimes cause programs to suspend. Its cause the sendall methods work principle. sendall method can not send all data at a time, it re-sends the remaining data. On client side, client reads re-send data as second number of public key. Thus, seerver hangs on handshake phase. This breaks handshake phases.
