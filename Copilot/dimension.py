# Python 3
# 编写一个方法，计算数组中各点之间的最大距离
# 输入参数是一个数组，数组元素是若干个二维坐标点
# 输出是一个整数，表示数组中各点之间的最大距离
# 例如输入：[[1,1],[3,3],[4,4],[5,5]]
# 输出：4

# 思路：计算每个点到其他点的距离，取最大值
# 两点之间的距离公式：sqrt((x1-x2)^2+(y1-y2)^2)

import math

def maxDistance(points):
    max = 0
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            distance = math.sqrt((points[i][0]-points[j][0])**2+(points[i][1]-points[j][1])**2)
            if distance > max:
                max = distance
    return max

if __name__ == '__main__':
    points = [[1,1],[3,3],[4,4],[5,5]]
    print(maxDistance(points))
    # 更多测试
    points = [[1,1],[3,3],[4,4],[5,5],[0,0]]
    print(maxDistance(points))
    points = [[1,1],[3,3],[4,4],[5,5],[0,0],[2,2]]
    print(maxDistance(points))
    points = [[1,1],[3,3],[4,4],[5,5],[0,0],[2,2],[6,6]]
    print(maxDistance(points))
