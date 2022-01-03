

from typing import List


def hamming(n: int) -> List[int]:
    """get a list of parity bit positions, given the number of parity bits."""
    r = []
    for i in range(n): 
        r.append(pow(2, i))
    return r


def xor(num: List[int]) -> int:
    """XOR the list of numbers."""
    r = 0
    for n in num:
        r = r ^ n
    return r 


def insert_zero(num: int, pos: int) -> int:
    mask = pow(2, pos - 1) - 1 
    t = num & mask
    num = (num >> (pos - 1)) << pos
    num = num + t
    return num


def setup(data: int, num_of_parity_bits: int) -> int:
    """create the bit positions first, set the parity bits to 0."""
    bits = hamming(num_of_parity_bits)
    for b in bits:
        data = insert_zero(data, b)
    return data


def pos(num: int) -> List[int]:
    """find the bit positions that have their bits set."""
    r = []
    for i in range(1, num.bit_length() + 1):
        if num & 1:
            r.append(i)
        num = num >> 1
    return r


def set_parity(bits, block, num_of_parity_bits: int) -> int:
    """set the parity bits, given the bits to set, and the block to set."""
    for i, n in enumerate(hamming(num_of_parity_bits)):
        if bits & pow(2, i):
            block = block | pow(2, n - 1)
    return block


def encode(d: int, num_of_parity_bits: int) -> int:
    data = setup(d, num_of_parity_bits)
    positions = pos(data)
    bits = xor(positions)
    encoded = set_parity(bits, data, num_of_parity_bits)
    return encoded


def flip(pos: int, data: int) -> int:
    """flip a bit in the data at a given position."""
    return data ^ (1 << pos - 1)


def remove_bit(num: int, pos: int):
    """remove bit at given position."""
    mask = pow(2, pos - 1) - 1
    t = num & mask
    num = (num >> pos) << (pos - 1)
    return num + t


def decode(e: int, num_parity_bits: int):
    c = xor(pos(e))
    if c: 
        e = flip(c, e) # flip the bit if there's an error  
    bits = hamming(num_parity_bits)
    bits.reverse()
    for b in bits:
        e = remove_bit(e, b)
    return e



if __name__ == "__main__":

    num_of_parity_bits = 4
    original =0b1001101
    print("original: {0:16b}".format(original))
    
    # encode original data with hamming
    encoded = encode(original, num_of_parity_bits)
    print("encoded : {0:16b}".format(encoded))

    # flip a bit at position 8 to create an error
    err = flip(8, encoded)
    print("error   : {0:16b}".format(err))

    # decode with correcting error
    decoded = decode(err, num_of_parity_bits)
    print("decoded : {0:16b}".format(decoded))



