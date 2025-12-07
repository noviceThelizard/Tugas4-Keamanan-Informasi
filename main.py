import socket
import rsa
import des
import math
import hashlib

def main():
    plaintext = "The brown fox jumps over the lazy dog"
    plainhash = hashlib.sha256(plaintext.encode()).hexdigest()
    
    e1, d1, n1 = rsa.generateKeys()
    e2, d2, n2 = rsa.generateKeys()
    base, modulus = 2, 19

    key = base**d1%modulus
    shared_keys = des.padding(str(key**d2%modulus))

    key_bin = des.str_to_bin(shared_keys.ljust(8))[:64]
    keys = des.keygen(key_bin)

    ds = []
    for i in range(0,8):
        ds.append(plainhash[i*8:i*8+8])
    
    for i in ds:
        print(i)
        
    bin = []
    for i in ds:
        bin.append(des.str_to_bin(i)[:64])

    encrypted = []
    for i in bin:
        encrypted.append(des.encrypt(i, keys))

    decrypted = []
    for i in encrypted:
        decrypted.append(des.decrypt(i, keys))

    for i in decrypted:
        print(des.bin_to_str(i))



main()