import socket
import rsas
import des
import math
import hashlib
import pickle

host = "localhost"
port = 80

def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    base, modulus = 2, 19
    
    # e, d, n = rsas.keygen()
    e,d,n = 3452821,6720421,7266359

    message = input("Enter the message: ")
    hash = hashlib.sha256(message.encode()).hexdigest()
    blocks, signed_blocks = rsas.sign(hash, d, n)
    print("hashed message (sha256)", hash)
    s.send(pickle.dumps(signed_blocks))
    s.send(message.encode())

    s.close()

main()