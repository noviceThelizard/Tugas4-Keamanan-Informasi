import socket
import rsa
import des

host = "localhost"
port = 80

def handle_client_connection(client_socket, addr):
    """Handle a single client connection."""
    print(f"Got a connection from {addr}")
    base, modulus = 2, 19
    e, d, n = rsa.generateKeys()

    recv_key = client_socket.recv(1024).decode()
    print(f"[Server] Received Key: {recv_key}")

    recv_key = int(recv_key)
    send_key = base**d%modulus

    client_socket.send(str(send_key).encode("utf-8"))
    print(f"[Server] Sending key: {send_key}")

    shared_key = des.padding(str(recv_key**d%modulus))
    print(f"[Server] Shared key created: {shared_key}")
    key_bin = des.str_to_bin(shared_key)
    keys = des.keygen(key_bin)

    msg = []
    length = client_socket.recv(1024).decode()
    length = int(length)
    for i in range(0,length):
        msg.append(client_socket.recv(1024).decode())

    bin = []
    for i in msg:
        bin.append(des.str_to_bin(i)[:64])

    encrypted = []
    for i in bin:
        encrypted.append(des.encrypt(i, keys))

    decrypted = []
    for i in encrypted:
        print(des.bin_to_hex(i))
        decrypted.append(des.decrypt(i, keys))

    for i in decrypted:
        print(des.bin_to_str(i))

    # close socket
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