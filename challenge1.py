from base64 import b16decode,b64encode

def hex_to_base64(data_hex: bytes) -> bytes:
    # data_hex = b"49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    return b64encode(b16decode(data_hex,casefold=True))


if __name__ == '__main__':
    data = b"49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    base_64_data = hex_to_base64(data)
    if not base_64_data == b'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t':
        exit('encoding failed')
    else:
        print(f'{hex_to_base64=}')
        print('successfully encoded')
