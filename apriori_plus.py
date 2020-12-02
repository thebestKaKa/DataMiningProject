# encoding:utf-8
# tqdm是进度条包
from tqdm import tqdm


# 遍历整个数据集生成c1候选集(set)
def create_c1(dataset):
    c1 = set()
    for i in dataset:
        for j in i:
            item = frozenset([j])
            c1.add(item)
    return c1


# 剪枝步
# 通过候选项ck生成lk(集合的集合)，并将各频繁项的支持度保存到support_data字典中
def generate_lk_by_ck(dataset, ck, min_support, support_data):
    item_count = {}  # 用于标记各候选项在数据集出现的次数
    Lk = set()
    for t in tqdm(dataset):  # 遍历数据集
        for item in ck:  # 检查候选集ck中的每一项是否出现在事务t中
            if item.issubset(t):
                if item not in item_count:
                    item_count[item] = 1
                else:
                    item_count[item] += 1
    for item in item_count:  # 将满足支持度的候选项添加到频繁项集中
        if item_count[item] >= min_support:
            Lk.add(item)
            support_data[item] = item_count[item]
    return Lk


# 连接步
# 通过频繁项集Lk-1创建ck候选项集
def create_ck(Lk_1, k):
    Ck = set()
    length = len(Lk_1)
    lk_list = list(Lk_1)
    for i in range(length):
        for j in range(i + 1, length):  # 两次遍历Lk-1，找出前n-1个元素相同的项
            l1 = list(lk_list[i])
            l2 = list(lk_list[j])
            l1.sort()
            l2.sort()
            if l1[0:k - 2] == l2[0:k - 2]:  # 只有最后一项不同时，生成下一候选项
                Ck_item = lk_list[i] | lk_list[j]
                if has_infrequent_subset(Ck_item, Lk_1):  # 检查该候选项的子集是否都在Lk-1中
                    Ck.add(Ck_item)
    return Ck


# 检查候选项Ck_item的子集是否都在Lk-1中
def has_infrequent_subset(Ck_item, Lk_1):
    for item in Ck_item:
        sub_Ck = Ck_item - frozenset([item])
        if sub_Ck not in Lk_1:
            return False
    return True


# 用于生成所有频繁项集的主函数，k为最大频繁项的大小
def generate_L(dataset, min_support):
    support_data = {}  # 用于保存各频繁项的支持度
    C1 = create_c1(dataset)  # 生成C1
    L1 = generate_lk_by_ck(dataset, C1, min_support, support_data)  # 根据C1生成L1
    Lk_1 = L1.copy()  # 初始时Lk-1=L1
    L = [Lk_1]
    i = 2
    while True:
        Ci = create_ck(Lk_1, i)  # 根据Lk-1生成Ck
        Li = generate_lk_by_ck(dataset, Ci, min_support, support_data)  # 根据Ck生成Lk
        if len(Li) == 0:
            break
        Lk_1 = Li.copy()  # 下次迭代时Lk-1=Lk
        L.append(Lk_1)
        i += 1
    for i in range(len(L)):
        print("frequent item {}：{}".format(i + 1, len(L[i])))
    return L, support_data


if __name__ == '__main__':
    support_data = {}
    min_support = 2
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
    L, support_data = generate_L(data_test, min_support)
    print('支持度字典：', support_data)
