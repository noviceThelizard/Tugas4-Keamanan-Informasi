from des_table import INIT_PERM, FINAL_PERM, PERM, EXP, SBOX, PC1, PC2, SHIFT_ROUND
import math

def str_to_bin(s):
    return ''.join(format(ord(c), '08b') for c in s)
def bin_to_str(b):
    return ''.join(chr(int(b[i:i + 8], 2)) for i in range(0, len(b), 8))
def bin_to_hex(b):
    return format(int(b, 2), '016x')
def hex_to_bin(h):
    return format(int(h, 16), '064b')
def permute(bits, table):
    return ''.join(bits[i - 1] for i in table)
def xor(a, b):
    return ''.join('0' if x == y else '1' for x, y in zip(a, b))
def shift(bits, n):
    return bits[n:] + bits[:n]

def str_to_list(s):
    out = []
    for i in s:
        out.append(i)
    return out
def list_to_str(l):
    out = ''
    for i in l:
        out = out+i
    return out

def sbox_substitution(bits):
    result = ''
    for i in range(8):
        block = bits[i * 6:(i + 1) * 6]
        row = int(block[0] + block[-1], 2)
        col = int(block[1:5], 2)
        val = SBOX[i][row][col]
        result += format(val, '04b')
    return result

def keygen(key):
    key = permute(key, PC1)
    # print("round - bits: "+key)
    c, d = key[:28], key[28:]
    keys = []
    for shifts in SHIFT_ROUND:
        c = shift(c, shifts)
        d = shift(d, shifts)
        keys.append(permute(c + d, PC2))
    return keys

def feistel(right, key):
    expanded = permute(right, EXP)
    xored = xor(expanded, key)
    substituted = sbox_substitution(xored)
    return permute(substituted, PERM)

def encrypt(block, keys):
    block = permute(block, INIT_PERM)
    l, r = block[:32], block[32:]
    for key in keys:
        l, r = r, xor(l, feistel(r, key))
    return permute(r + l, FINAL_PERM)

def decrypt(block, keys):
    block = permute(block, INIT_PERM)
    l, r = block[:32], block[32:]
    for key in reversed(keys):
        l, r = r, xor(l, feistel(r, key))
    return permute(r + l, FINAL_PERM)

def padding(data):
    result = data
    while len(result) < 8:
        result = '0'+result
    return result

'''
def main():
    plaintxt = "mikoyanagurevichsukhoii"
    key = "gurevich"
    blocks = math.ceil(len(plaintxt)/8)
    message = []
    for i in range(0,blocks):
        buffer = plaintxt[i*8:i*8+8]
        if len(buffer) < 8:
            buffer = padding(buffer)
        message.append(buffer)
        print(message[i])


    print("plaintext: "+plaintxt)

    pt_bin = str_to_bin(plaintxt.ljust(8))[:64]
    print(pt_bin)
    key_bin = str_to_bin(key.ljust(8))[:64]
    keys = keygen(key_bin)
    encrypted = encrypt(pt_bin, keys)
    print("ciphertext:"+bin_to_hex(encrypted))
    
    key_bin = str_to_bin(key.ljust(8))[:64]
    keys = keygen(key_bin)
    decrypted = decrypt(encrypted, keys)
    plaintext = bin_to_str(decrypted)
    print("decryptedtext:"+plaintext)

main()

'''