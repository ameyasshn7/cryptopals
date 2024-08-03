from typing import List

BLOCK_SIZE = 16

def bytes_to_chunks(b: bytes, chunk_size: int, quiet=True) -> List[bytes]:
    chunks = [b[ind:ind+chunk_size] for ind in range(0,len(b), chunk_size)]
    if not quiet:
        print(f"Input converted to chunks of size {chunk_size}:{chunks}")

    return chunks

if __name__ == '__main__':
    with open('8.txt') as f:
        ciphertext = [bytes.fromhex(line.strip()) for line in f]

    for i, ciphertext in enumerate(ciphertext):
        num_blocks = len(ciphertext) // BLOCK_SIZE
        unique_blocks = len(set(bytes_to_chunks(ciphertext, BLOCK_SIZE)))
        repeated_blocks = num_blocks - unique_blocks

        if repeated_blocks == 0:
            continue

        print(f'Line {i} has a {repeated_blocks} repeated blocks')