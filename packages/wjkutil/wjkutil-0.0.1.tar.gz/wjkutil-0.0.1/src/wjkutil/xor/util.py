def bxor(a, b):     # xor two byte strings of different lengths
    if len(a) != len(b):
        print("bxor: warning! bxor two bytes's lengths are not equal")
    if len(a) > len(b):
        return bytes([x ^ y for x, y in zip(a[:len(b)], b)])
    else:
        return bytes([x ^ y for x, y in zip(a, b[:len(a)])])

def hamming_distance(b1, b2):
    differing_bits = 0
    for byte in bxor(b1, b2):
        differing_bits += bin(byte).count("1")
    return differing_bits

def hamming_distance_iter(chaine1, chaine2):
    """
    两iter中!=的数量
    eg: 计算两字符串/bytes中不同的数目. 用于计算密钥错误数
    """
    assert(len(chaine1) == len(chaine2))
    return sum(c1 != c2 for c1, c2 in zip(chaine1, chaine2))
