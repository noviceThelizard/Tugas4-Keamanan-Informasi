import random
import math

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_random_prime(start, end):
    while True:
        num = random.randint(start, end)
        if is_prime(num):
            return num
        
def split_into_blocks(message, block_size):
    return [message[i : i + block_size] for i in range(0, len(message), block_size)]

def encrypt_block(block, d, n):
    block_int = int.from_bytes(block.encode("utf-8"), byteorder="big")
    encrypted_block_int = pow(block_int, d, n)
    return encrypted_block_int

def sign(message, d, n):
    block_size = ((n.bit_length() - 1) // 8)
    if len(message) <= block_size:
        return [encrypt_block(message, d, n)]
    else:
        blocks = split_into_blocks(message, block_size)
        signed_blocks = [encrypt_block(block, d, n) for block in blocks]
        return blocks, signed_blocks

def decrypt_block(encrypted_block_int, e, n):
    decrypted_block_int = pow(encrypted_block_int, e, n)
    decrypted_block_bytes = decrypted_block_int.to_bytes(
        (decrypted_block_int.bit_length() + 7) // 8, byteorder="big"
    )
    return decrypted_block_bytes.decode("utf-8")

def verify(signed_blocks, e, n, original_message):
    decrypted_blocks = [
        decrypt_block(signed_block, e, n) for signed_block in signed_blocks
    ]
    decrypted_message = "".join(decrypted_blocks)
    return decrypted_message == original_message

def modInverse(e, phi):
    for d in range(2, phi):
        if (e * d) % phi == 1:
            return d
    return -1

def keygen():
    # RSA Key Generation
    p, q = generate_random_prime(3, 5000), generate_random_prime(3, 5000)
    while p == q:
        q = generate_random_prime(3, 47)

    n = p * q
    totient_n = (p - 1) * (q - 1)

    # Find a number "e" that is coprime to the "totient_n"
    e = random.randint(3, totient_n - 1)

    while math.gcd(e, totient_n) != 1:
        e = random.randint(3, totient_n - 1)

    d = modInverse(e, totient_n)

    return e,d,n

    # print(f"\nPublic Key:{e}\nPrivate Key:{d}\nn:{n}\nPhi of n:{totient_n}\np:{p}\nq:{q}\n\n")

    # message = input("Enter the message: ")
    # blocks, signed_blocks = sign(message, d, n)
    # verification_result = verify(signed_blocks, e, n, message)

    # blocks_str = "".join(blocks)
    # signed_blocks_str = " ".join(map(str, signed_blocks))
    # signed_message = blocks_str + " | " + signed_blocks_str


    # print("\nSeperated message:", blocks)
    # print("Signed blocks:", signed_blocks)
    # print("Signed message:", signed_message)
    # print("Verification result:", verification_result)

def main():
    e,d,n = keygen()

    print(f"\nPublic Key:{e}\nPrivate Key:{d}\nn:{n}\n")
    message = input("Enter the message: ")
    blocks, signed_blocks = sign(message, d, n)
    print(type(signed_blocks))
    verification_result = verify(signed_blocks, e, n, message)

    blocks_str = "".join(blocks)
    signed_blocks_str = " ".join(map(str, signed_blocks))
    signed_message = blocks_str + " | " + signed_blocks_str

    print("\nSeperated message:", blocks)
    print("Signed blocks:", signed_blocks)
    print("Signed message:", signed_message)
    print("Verification result:", verification_result)
    

# main()