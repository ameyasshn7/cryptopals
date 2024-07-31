class PaddingError(Exception):
    pass

def pkcs7(b: bytes, block_size: int = 16) -> bytes:
    if block_size == 16:
        pad_len = block_size - (len(b) & 15)
    else:
        pad_len = block_size - (len(b) % block_size)
    
    return b + bytes([pad_len]) * pad_len


def strip_pkcs7(b: bytes) -> bytes:
    n = b[-1]

    if n == 0 or len(b) < n or b[-n:] != bytes([n]) * n:
        raise PaddingError

    return b[:-n]

if __name__ == '__main__':
    plain_text = b"YELLOW SUBMARINE"
    padded = pkcs7(plain_text, block_size=20)
    unpadded = strip_pkcs7(padded)

    if padded != b"YELLOW SUBMARINE\x04\x04\x04\x04":
        print('ERROR: Padding did not work')
        exit()
    if unpadded != plain_text:
        print('ERROR: unpadding did not work')
        exit()
    
    print(f'{padded=}')
    print(f'{unpadded=}')