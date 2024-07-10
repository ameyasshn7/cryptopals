from collections import Counter
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from pprint import pprint
from dataclasses import dataclass, astuple
from typing import Optional
from challenge2 import bytes_xor
from read_book import get_freqs

frequencies_ ={'a': 0.0774934698168604, 'b': 0.014035108384843497, 'c': 0.02665963831472685, 'd': 0.04923478327448561, 
              'e': 0.13462925934324174, 'f': 0.025078259128268405, 'g': 0.016965224382098906, 'h': 0.057126955005786614, 
              'i': 0.0630490286444606, 'j': 0.0012692261254443028, 'k': 0.005071014821380718, 'l': 0.037113821018502434, 
              'm': 0.03031712984094918, 'n': 0.07131813992113718, 'o': 0.07376530212588014, 'p': 0.017489405937386807, 
              'q': 0.0009511833840336654, 'r': 0.06097586114489497, 's': 0.06127329000491788, 't': 0.08747353324871826, 
              'u': 0.03044964764987028, 'v': 0.011155054670958281, 'w': 0.02160040285413912, 'x': 0.0019877671338164836, 
              'y': 0.02280189765502375, 'z': 0.000715596168173934}

frequencies = get_freqs('frankenstein.txt',ascii_lowercase)

@dataclass
class ScoredGuess:
    score: float = float("inf")
    key: Optional[int] = None
    ciphertext: Optional[bytes] = None
    plaintext: Optional[bytes] = None

    def __lt__(self, other):
        return self.score < other.score

    @classmethod
    def from_key(cls, ct, key_val):
        full_key = bytes([key_val]) * len(ct)
        pt = bytes_xor(ct, full_key)
        score = score_text(pt)
        return cls(score, key_val, ct, pt)

def score_text(text: bytes) -> float:
    score = 0.0
    l = len(text)
    for letter, expected_frequency in frequencies.items():
        actual_frequency = text.count(ord(letter)) / l
        err = abs(expected_frequency - actual_frequency)
        score += err
    return score

def crack_xor_cipher(ciphertext: bytes) -> ScoredGuess:
    best_guess = ScoredGuess()

    for candidate_key in range(256):
        guess = ScoredGuess.from_key(ciphertext, candidate_key)
        best_guess = min(best_guess, guess)
    
    if best_guess.key is None or best_guess.plaintext is None:
        exit('no key found')

    return best_guess

if __name__ == '__main__':
    ciphertext = bytes.fromhex('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
    best_guess = crack_xor_cipher(ciphertext)
    score,key,ciphertext,plaintext = astuple(best_guess)
    print(score,key,ciphertext,plaintext)
