from base64 import b64decode

from challenge2 import bytes_xor
from challenge7 import aes_ecb_dec, AES
from challenge8 import bytes_to_chunks
from challenge9 import strip_pkcs7

KEY = b"YELLOW SUBMARINE"
BLOCK_SIZE = AES.block_size
def aes_cbc_dec(iv: bytes, key: bytes, ciphertext: bytes, use_pkcs7=True):
    blocks = bytes_to_chunks(ciphertext, BLOCK_SIZE)
    prev_ciphertext = iv
    plaintext = b''
    
    for block in blocks:
        raw_dec = aes_ecb_dec(key, block)
        plaintext += bytes_xor(raw_dec, prev_ciphertext)
        prev_ciphertext = block

    if use_pkcs7:
        plaintext = strip_pkcs7(plaintext)
    return plaintext


if __name__ == "__main__":

    with open('10.txt') as f:
        b64_data = f.read()

    ciphertext = b64decode(b64_data)

    iv = bytes(BLOCK_SIZE)
    key = KEY
    plaintext = bytes(aes_cbc_dec(iv,key,ciphertext,True))

    print(plaintext.decode("ascii"))
