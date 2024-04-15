"""
假设各种长度的汉明距离, 输出最高的几个可能的长度
支持base64, hex, binary格式, 文件输入.
猜测密钥长度
将两个二进制的字符异或后计算值为1的比特位个数，就是汉明距离。
正常英文字母的平均汉明距离较小(2-3), 随机字节的汉明距离平均是4. 被相同字符加密的密文与密文之间的汉明距离等于明文与明文之间的汉明距离.
这样对每个假设的长度计算汉明距离, 并且找最小的.
由定义也可以发现, 长度的因数的汉明距离也会稍大一些.
"""
from .util import hamming_distance, bxor

def old_guess_len(b):
    """
    https://www.anquanke.com/post/id/161171#h3-6
    original version of guess length of xored bytes
    硬取前6段的
    """
    normalized_distances = []

    for KEYSIZE in range(2, 40):
        #我们取其中前6段计算平局汉明距离
        b1 = b[: KEYSIZE]
        b2 = b[KEYSIZE: KEYSIZE * 2]
        b3 = b[KEYSIZE * 2: KEYSIZE * 3]
        b4 = b[KEYSIZE * 3: KEYSIZE * 4]
        b5 = b[KEYSIZE * 4: KEYSIZE * 5]
        b6 = b[KEYSIZE * 5: KEYSIZE * 6]

        normalized_distance = float(
            hamming_distance(b1, b2) +
            hamming_distance(b2, b3) +
            hamming_distance(b3, b4) +
            hamming_distance(b4, b5) + 
            hamming_distance(b5, b6) 
        ) / (KEYSIZE * 5)

        normalized_distances.append(
            (KEYSIZE, normalized_distance)
        )
    normalized_distances = sorted(normalized_distances,key=lambda x:x[1])
    return normalized_distances

def guess_len(b):
    """
    取9段或者更少(不够), 两两计算汉明距离再求平均...
    """
    normalized_distances = []

    for key_size in range(2, 40):
        chops_num = len(b) // key_size # 取最多chops段
        chops_num = min([chops_num, 9])
        chops = [b[key_size * i:key_size * (i + 1)] for i in range(chops_num)]

        total_distance = 0.0
        count = 0
        from itertools import combinations
        for b1, b2 in combinations(chops, 2): # 两两组合计算汉明距离
            count += 1
            total_distance += hamming_distance(b1, b2)
        normalized_distance = total_distance / (key_size * count)

        normalized_distances.append(
            (key_size, normalized_distance)
        )
    normalized_distances = sorted(normalized_distances,key=lambda x:x[1])
    return normalized_distances

if __name__ == '__main__':
    import codecs
    enc = '1e5d4c055104471c6f234f5501555b5a014e5d001c2a54470555064c443e235b4c0e590356542a130a4242335a47551a590a136f1d5d4d440b0956773613180b5f184015210e4f541c075a47064e5f001e2a4f711844430c473e2413011a100556153d1e4f45061441151901470a196f035b0c4443185b322e130806431d5a072a46385901555c5b550a541c1a2600564d5f054c453e32444c0a434d43182a0b1c540a55415a550a5e1b0f613a5c1f10021e56773a5a0206100852063c4a18581a1d15411d17111b052113460850104c472239564c0755015a13271e0a55553b5a47551a54010e2a06130b5506005a393013180c100f52072a4a1b5e1b165d50064e411d0521111f235f114c47362447094f10035c066f19025402191915110b4206182a544702100109133e394505175509671b6f0b01484e06505b061b50034a2911521e44431b5a233f13180b5508131523050154403740415503484f0c2602564d470a18407b775d031110004a54290319544e06505b060b424f092e1a770443101952333213030d554d551b2006064206555d50141c454f0c3d1b5e4d43061e453e39544c17580856581802001102105443101d111a043c03521455074c473f3213000a5b085d113c194f5e08555415180f5f433e270d131d420c1957773f560d11440d40543c060e470b55545b114e470e193c155f4d47110947343f13180c100f565a000403484e184c15050250081f2a54470545104c5536251325435302461a3b4a02484e12545c1b4265070b3b5440055543185b36231301025b084054220f4f42071b1554020f430b196f19564d4002055d79'
    b = codecs.decode(enc, 'hex')
    print(guess_len(b))
