import socket
import rsa
import des
import math
import hashlib

host = "localhost"
port = 80

def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    base, modulus = 2, 19
    
    e, d, n = rsa.generateKeys()

    key = base**d%modulus
    print(f"[Client] Sending Key: {key}")
    s.send(str(key).encode("utf-8"))
    recv_key = int(s.recv(1024).decode("utf-8"))
    print(f"[Client] Receiving Key: {recv_key}")

    shared_key = des.padding(str(recv_key**d%modulus))
    print(f"[Client] Shared key created: {shared_key}")
    key_bin = des.str_to_bin(shared_key.ljust(8))[:64]
    keys = des.keygen(key_bin)


    plain = "usernamepasswordgurevich"
    plain_hash = hashlib.sha256(plain.encode()).hexdigest()
    msg = []
    s.send(str(math.ceil(len(plain)/8)).encode())
    for i in range(0, math.ceil(len(plain)/8)):
        msg.append(plain[i*8:i*8+8])
        s.send(plain[i*8:i*8+8].encode())
        
    # s.send(msg.encode())
    
    msg_hash = []
    for i in range(0, 8):
        msg_hash.append(plain_hash[i*8:i*8+8])
    
    digital_signature = ""
    for i in msg_hash:
        digital_signature = digital_signature+des.bin_to_hex(des.encrypt(i, keys))

    print(digital_signature)
    s.close()

main()