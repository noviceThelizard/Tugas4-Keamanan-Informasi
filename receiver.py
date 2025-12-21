import socket
import rsas
import des
import pickle
import hashlib

host = "localhost"
port = 80

def handle_client_connection(client_socket, addr):
    """Handle a single client connection."""
    print(f"Got a connection from {addr}")
    base, modulus = 2, 19
    
    e,d,n = 3452821,6720421,7266359

    signed_blocks = pickle.loads(client_socket.recv(1024))
    message = client_socket.recv(1024)
    print("message received:", message.decode())
    verification_result = rsas.verify(signed_blocks, e, n, hashlib.sha256(message).hexdigest())

    decrypted_blocks = [
        rsas.decrypt_block(signed_block, e, n) for signed_block in signed_blocks
    ]
    decrypted_message = "".join(decrypted_blocks)

    print("hashed message", hashlib.sha256(message).hexdigest())
    print("signed message", decrypted_message)
    print("verification result: ",verification_result)
    
    client_socket.close()

def main():
    key = "12345678"

    key_bin = des.str_to_bin(key)

    keys = des.keygen(key_bin)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((host, port))

    s.listen(5)

    try:
        while True:
            # accept connection
            client_socket, addr = s.accept()

            # handle connection
            handle_client_connection(client_socket, addr)
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        # close 
        s.close()

    s.close()

main()