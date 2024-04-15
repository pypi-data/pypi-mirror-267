# 破解单字节异或
from .util import bxor

# -------------空格攻击------------------------

def space_only(text):
    """
    精确猜测空格
    需要猜测成功长度. 得到被相同字符加密的密文分组
        1. 密文和密文异或等于明文和明文异或.
        2. 空格和所有小写字母异或结果是相应的大写字母，空格和所有大写字母异或是相应的小写字母。
    利用单组之间各个字符相互异或, 如果某个字符和其他字符异或, 大部分在字母区间内, 则说明这个字符大概率是空格. 
    找出空格则可以找到对应的密钥字节. 密文很多时单靠这种方法就甚至可以破解.
    对单个分组内, 依次假设每个密文对应的明文是空格. 计算该密文异或其他密文, 结果落在字母范围内的次数. 找出次数最多的那个, 作为明文是空格的, 得到对应的密文字符.
    """
    key = 0
    possible_space=0
    max_possible=0
    import string
    letters = string.ascii_letters.encode('ascii')
    for a in range(0, len(text)):
        maxpossible = 0
        for b in range(0, len(text)):
            if(a == b):
                continue
            c = text[a] ^ text[b]
            if c not in letters and c != 0:
                continue
            maxpossible += 1
        if maxpossible>max_possible:
            max_possible=maxpossible
            possible_space=a
    key = text[possible_space]^ 0x20
    return bytes([key])

# -----------freq_attack--------------
# -----------频率攻击---------------
freq = {}
freq[' '] = 700000000
freq['e'] = 390395169
freq['t'] = 282039486
freq['a'] = 248362256
freq['o'] = 235661502
freq['i'] = 214822972
freq['n'] = 214319386
freq['s'] = 196844692
freq['h'] = 193607737
freq['r'] = 184990759
freq['d'] = 134044565
freq['l'] = 125951672
freq['u'] = 88219598
freq['c'] = 79962026
freq['m'] = 79502870
freq['f'] = 72967175
freq['w'] = 69069021
freq['g'] = 61549736
freq['y'] = 59010696
freq['p'] = 55746578
freq['b'] = 47673928
freq['v'] = 30476191
freq['k'] = 22969448
freq['x'] = 5574077
freq['j'] = 4507165
freq['q'] = 3649838
freq['z'] = 2456495

def score(s):
    # 计算byte array的score
    score = 0
    string=bytes.decode(s, 'latin1')
    for c in string.lower():
        if c in freq:
            score += freq[c]
    return score

def freq_only(b1):
    """
    只利用词频计算积分的方法攻击单字节异或
    词频攻击:
    也需要成功猜测长度, 分组. 这样单个分组的密文就是类似于单表代换了. 使用词频分析法. 单个分组的密文越多越靠谱. 给每个明文字母(大小写相同分数)和空格一个分数.
    对每个分组, 遍历256种密文的假设, 计算明文的分数, 找出分数最大的即可.
    """
    max_score = 0
    english_plaintext = 0
    key = 0

    for i in range(0,256):
        b2 = [i] * len(b1)
        try:
            plaintext = bxor(b1, b2)
            pscore = score(plaintext)
        except Exception as e:
            print(e)
            continue
        if pscore > max_score or not max_score:
            max_score = pscore
            english_plaintext = plaintext
            key = i
    return bytes([key])
