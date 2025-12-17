import socket
import rsa
import des
import math
import hashlib

def str_to_num(string):
    numstring = ""
    for i in string:
        nextnum = str(ord(i))
        while len(nextnum) < 3:
            nextnum = '2'+nextnum
        numstring = numstring+nextnum
    return numstring


def padding(data):
    result = data
    while len(result) < 7:
        result = result+'0'
    return result


def sign_message(plaintext, e, n):
    plainhash = hashlib.sha256(plaintext.encode()).hexdigest()
    hashnum = str_to_num(plainhash)
    print(hashnum, len(hashnum))
    length_of_hashnum = len(hashnum)/7
    signature = ""
    iteration = 0
    if math.floor(length_of_hashnum) == len(hashnum)/7:
        iteration = math.floor(length_of_hashnum)
    else:
        iteration = math.floor(length_of_hashnum)+1

    for i in range(0,iteration):
        next_hash = padding(hashnum[i*7:i*7+7])
        next_encrypt = rsa.encrypt(int(next_hash),e,n)
        # print(i,next_hash,i*7)
        # print(i,padding(str(next_encrypt)), len(str(next_encrypt)))
        signature += padding(str(next_encrypt))
        # print(i,signature, len(signature))
    return signature

def verify_message(signature, message, d, n):
    length_of_signature = len(signature)/7
    iteration = 0
    if math.floor(length_of_signature) == len(signature)/7:
        iteration = math.floor(length_of_signature)
    else:
        iteration = math.floor(length_of_signature)+1
    
    return

def main():
    plaintext = "The brown fox jumps over the lazy dog"
    
    
    e,d,n = 3, 3135299, 4707673
    
    signature = sign_message(plaintext, e, n)
    print(signature, len(signature))
    
    verification = False

    e1, d1, n1 = rsa.generateKeys()
    e2, d2, n2 = rsa.generateKeys()
    base, modulus = 2, 19

    key = base**d1%modulus
    shared_keys = des.padding(str(key**d2%modulus))

    key_bin = des.str_to_bin(shared_keys.ljust(8))[:64]
    keys = des.keygen(key_bin)
    m = 1234567

    encrypted = rsa.encrypt(m,e,n)
    print(encrypted)
    decrypted = rsa.decrypt(encrypted,d,n)
    print(decrypted)
    # ds = []
    # for i in range(0,8):
    #     ds.append(plainhash[i*8:i*8+8])
    
    # for i in ds:
    #     print(i)
        
    # bin = []
    # for i in ds:
    #     bin.append(des.str_to_bin(i)[:64])

    # encrypted = []
    # for i in bin:
    #     encrypted.append(des.encrypt(i, keys))

    # decrypted = []
    # for i in encrypted:
    #     decrypted.append(des.decrypt(i, keys))

    # for i in decrypted:
    #     print(des.bin_to_str(i))



main()