from collections import Counter
from string import ascii_letters, ascii_lowercase, ascii_uppercase




def get_freqs(letters):
    with open('frankenstein.txt') as f:
        book = f.read()
    counts = Counter()
    for letter in letters:
        counts[letter] += book.count(letter)
    
    total = sum(counts.values())

    return( {letter: counts[letter] / total for letter in letters})


if __name__ == '__main__':
    print(get_freqs(ascii_lowercase))