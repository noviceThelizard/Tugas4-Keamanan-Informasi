# Python Program for implementation of RSA Algorithm
import random

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

def power(base, expo, m):
    res = 1
    base = base % m
    while expo > 0:
        if expo & 1:
            res = (res * base) % m
        base = (base * base) % m
        expo = expo // 2
    return res

# Function to find modular inverse of e modulo phi(n)
# Here we are calculating phi(n) using Hit and Trial Method
# but we can optimize it using Extended Euclidean Algorithm
def modInverse(e, phi):
    for d in range(2, phi):
        if (e * d) % phi == 1:
            return d
    return -1

# RSA Key Generation
def generateKeys():
    p = generate_random_prime(1024,4096)
    q = generate_random_prime(1024,4096)
    
    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e, where 1 < e < phi(n) and gcd(e, phi(n)) == 1
    e = 0
    for e in range(2, phi):
        if gcd(e, phi) == 1:
            break

    # Compute d such that e * d ≡ 1 (mod phi(n))
    d = modInverse(e, phi)

    return e, d, n

# Function to calculate gcd
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Encrypt message using public key (e, n)
def encrypt(m, e, n):
    return power(m, e, n)

# Decrypt message using private key (d, n)
def decrypt(c, d, n):
    return power(c, d, n)

# Main execution
if __name__ == "__main__":
    
    # Key Generation
    e, d, n = generateKeys()
  
    print(f"Public Key (e, n): ({e}, {n})")
    print(f"Private Key (d, n): ({d}, {n})")

    # Message
    M = 123
    print(f"Original Message: {M}")

    # Encrypt the message
    C = encrypt(M, e, n)
    print(f"Encrypted Message: {C}")

    # Decrypt the message
    decrypted = decrypt(C, d, n)
    print(f"Decrypted Message: {decrypted}")