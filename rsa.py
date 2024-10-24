import random
#bikin sendiri bos

def fpb(a,b): 
    if a == 0:
        return b
    return fpb(b%a,a)


def gcdExtended(a, b):  
    if a == 0 : 
        return b,0,1
             
    gcd,x1,y1 = gcdExtended(b%a, a) 
    x = y1 - (b//a) * x1 
    y = x1 
     
    return gcd,x,y 


def isPrime(x):
    if x == 1 or x == 0:
        return False
    for i in range(2,x):
        if x % i == 0:
            return False
    return True


def divideString(message):
    message_length = len(message)
    div_message = []
    string = ""
    count = 0
    alphabet_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    for kata in message:
        jadi_angka = alphabet_list.index(kata) % 26
        if jadi_angka < 10:
            string += "0"
        string += str(jadi_angka)
        count += 1
        if count == 2:
            div_message.append(int(string))
            count = 0
            string = ""

    if message_length % 2 != 0:
        jadi_angka = alphabet_list.index(message[message_length-1]) % 26
        div_message.append(jadi_angka)

    return div_message

def generate_prime_candidate(length):
    p = random.getrandbits(length)
    return p | (1 << length - 1) | 1

def generate_prime_number(length):
    p = 4
    while not isPrime(p):
        p = generate_prime_candidate(length)
    return p

def generate_keys(length,e):
    p = generate_prime_number(length)
    q = generate_prime_number(length)
    n = p*q
    if fpb(e,(p-1)*(q-1)) != 1:
        raise ValueError("Values can't be encrypted")
    
    return n,p,q

def encrypt(length,message,e):
    n,p,q = generate_keys(length,e)
    plaintext = divideString(message)
    ciphertext = ""
    for x in range(len(divideString(message))):
        hasil = (plaintext[x]**e)%n
        ciphertext += str(hasil)
    return ciphertext
