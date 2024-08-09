from os import urandom
from random import choice, randint
from typing import Callable
from typing import Tuple

from Crypto.Cipher import AES

from challenge8 import bytes_to_chunks
from challenge9 import pkcs7

EncOracType = Callable[[bytes],bytes]
BLOCK_SIZE = AES.block_size
KEY_SIZE = 16

def get_encryption_oracle() -> Tuple[str,EncOracType]:   
    mode = choice(("ECB","CBC"))

    def encryption_oracle(plaintext: bytes) -> bytes:
        key = urandom(KEY_SIZE)         #generating random keys
        prefix = urandom(randint(5,10))
        postfix = urandom(randint(5,10))

        plaintext = pkcs7(prefix + plaintext + postfix)

        if mode == "ECB":
            cipher = AES.new(key, AES.MODE_ECB)
        else:
            iv = urandom(BLOCK_SIZE)
            cipher = AES.new(key,AES.MODE_CBC, iv)
        
        return cipher.encrypt(plaintext)
    return mode, encryption_oracle

def detector(func: EncOracType) -> str:
    plaintext = bytes(2*BLOCK_SIZE + (BLOCK_SIZE-5))
    ciphertext = func(plaintext)
    ct_blocks = bytes_to_chunks(ciphertext, BLOCK_SIZE)

    if ct_blocks[1] == ct_blocks[2]:
        return "ECB"
    else:
        return "CBC"

if __name__ == '__main__':

    for _ in range(1000):
        _mode, oracle = get_encryption_oracle()
        guess = detector(oracle)
        print("Actual:", _mode, "Guessed", guess)
        if _mode != guess:
            raise Exception("Wrong!!!")
    
    print("Success")