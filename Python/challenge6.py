from challenge2 import bytes_xor
from challenge3 import crack_xor_cipher
from typing import Dict, List, Tuple
from itertools import combinations
from base64 import b16decode,b64encode 
import pprint

def hamming_distance(a: bytes,b: bytes) -> int:
    return sum(weights[byte] for byte in bytes_xor(a,b))

def _get_hamming_weights() -> Dict[int,int]:
    weights = {0:0}
    pow_2 = 1
    for _ in range(8):
        for k,v in weights.copy().items():
            weights[k+pow_2] = v+1

        pow_2 <<= 1
    
    return weights

weights = _get_hamming_weights()

MAX_KEYSIZE = 40
def guess_keysize(ct: bytes, num_guesses: int = 1) -> List[Tuple[float,int]]:
    def get_scores(size: int) -> float:
        chunks = (ct[:size], 
                  ct[size:2*size],
                  ct[2*size:3*size],
                  ct[3*size: size])
        avg = sum(hamming_distance(a,b) for a,b in combinations(chunks,2)) / 6
        return avg / size
    scores = [(get_scores(size), size) for size in range(2,MAX_KEYSIZE+1)]
    scores.sort()
    return scores[:num_guesses]

def crack_repeating_key_xor(ciphertext: bytes, keysize: int) -> Tuple[float, bytes]:
    chunks = [ciphertext[i::keysize] for i in range(keysize)]
    cracks = [crack_xor_cipher(chunk) for chunk in chunks]

    combined_scores = sum(guess.score for guess in cracks)
    key = bytes(guess.key for guess in cracks)
    return combined_scores , key

if __name__ == '__main__':
    print(hamming_distance(b'this is a test', b'wokka wokka!!!'))

    if hamming_distance(b'this is a test', b'wokka wokka!!!') != 37:
        exit('something went wrong')


    with open('6.txt') as f:
        b64 = f.read()
    
    ciphertext = b64encode(b64)
    keysizes = guess_keysize(ciphertext,5)
    pprint('best keysize guesses (confidence, size):')
    pprint(keysizes)

    candidates =  [crack_repeating_key_xor(ciphertext, guess) for _,guess in keysizes]
    candidates.sort()
    best_candidate = candidates[0]
    best_key = best_candidate[1]

    print('top guess :')
    print(f'{best_key=}')
    print('plaintext = \n')
    print(crack_repeating_key_xor(best_key,ciphertext).decode('ascii'))




    