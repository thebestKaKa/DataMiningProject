# encoding:utf-8
import csv


# data:二维列表
def apriori(data, min_support, min_confidence):
    frequent_item_sets = {}
    association_rules = []
    # 挖掘频繁1项集
    c_1 = {}
    for goods in data:
        for good in goods:
            if good in c_1.keys():
                c_1[good] = c_1[good] + 1
            else:
                c_1[good] = 1
    cutKeys(c_1, min_support)
    l_1 = c_1
    print(l_1)
    c_2 = apriori_gen(l_1)
    # print(c_2)
    c_2 = c_count(c_2, data)
    # print(c_2)
    cutKeys(c_2, min_support)
    l_2 = c_2
    print(l_2)


# 连接步
def apriori_gen(l_k):
    c_k_next = []
    for item1 in l_k:
        for item2 in l_k:
            temp = []
            if item1 != item2:
                temp.append(item1)
                temp.append(item2)
                temp.sort()
                if temp not in c_k_next:
                    c_k_next.append(temp)
    return c_k_next


# 剪枝步
def cutKeys(c_k, min_support):
    for i in list(c_k):
        if c_k[i] < min_support:
            c_k.pop(i)


# 将预备集转为字典 并计数
def c_count(c, data):
    c_k = {}
    for element in c:
        count = 0
        for item in data:
            if set(element).issubset(set(item)):
                count += 1
        c_k[str(element)] = count
    return c_k


lists = csv.reader(open('./groceries/groceries.csv', 'r', encoding='utf-8-sig'))
data = []
for goods in lists:
    good_new = []
    for good in goods:
        if len(good):
            good_new.append(good.strip())
    data.append(good_new)
data_test = [
    [1, 2, 5],
    [2, 4],
    [2, 3],
    [1, 2, 4],
    [1, 3],
    [2, 3],
    [1, 3],
    [1, 2, 3, 5],
    [1, 2, 3]
]
apriori(data_test, 2, 1)
