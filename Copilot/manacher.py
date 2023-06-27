# Manacher算法，找到输入字符串中最长在回文子字符串
# 时间复杂度: O(n)
# 空间复杂度: O(n)

def manacher(s):
    # 预处理字符串
    s = '#' + '#'.join(s) + '#'
    # RL数组
    RL = [0] * len(s)
    # 当前最右回文串的中心位置，及其右边界
    pos, max_right = 0, 0
    # 最长回文串的中心位置，及其长度
    max_pos, max_len = 0, 0
    for i in range(len(s)):
        # 初始化RL[i]
        if i < max_right:
            RL[i] = min(RL[2 * pos - i], max_right - i)
        else:
            RL[i] = 1
        # 尝试扩展RL[i]
        while i - RL[i] >= 0 and i + RL[i] < len(s) and s[i - RL[i]] == s[i + RL[i]]:
            RL[i] += 1
        # 更新pos和max_right
        if RL[i] + i - 1 > max_right:
            max_right = RL[i] + i - 1
            pos = i
        # 更新max_pos和max_len
        if RL[i] > max_len:
            max_len = RL[i]
            max_pos = i
    # 返回最长回文子串
    return s[max_pos - max_len + 1:max_pos + max_len:2]

   
# 单元测试
def manacher_test():
    print(manacher('abba'))
    print(manacher('abababa'))
    print(manacher('abcbabcbabcba'))
    print(manacher('测试中文文中有多少字符？'))


if __name__ == '__main__':
    manacher_test()