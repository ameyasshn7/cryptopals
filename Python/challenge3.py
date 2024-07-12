from collections import Counter
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from pprint import pprint
from dataclasses import dataclass, astuple
from typing import Optional
from challenge2 import bytes_xor
from read_book import get_freqs

frequencies = get_freqs(ascii_lowercase)

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
