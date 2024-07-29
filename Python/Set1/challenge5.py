from itertools import cycle, islice
from challenge2 import bytes_xor

def repeatingKeyXOR(key: bytes, plaintext: bytes) -> bytes:
    full_key = bytes(islice(cycle(key), len(plaintext)))
    return bytes_xor(full_key, plaintext)


if __name__ == '__main__':
    plaintext = (b"Burning 'em, if you ain't quick and nimble\n"
                    b"I go crazy when I hear a cymbal")

    expected = bytes.fromhex("0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272"
                            "a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f")

    key = b"ICE"
    
    ciphertext = repeatingKeyXOR(key, plaintext)
    print(f'{ciphertext.hex()=}')
    if ciphertext == expected:
        print('It worked!!')
    else:
        exit('Error encoding')


