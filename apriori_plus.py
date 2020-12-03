# encoding:utf-8
# tqdm是进度条包
import os

from tqdm import tqdm


# 遍历整个数据集生成c1候选集(set)
def create_c1(dataset):
    c1 = set()
    for i in dataset:
        for j in i:
            item = frozenset([j])
            c1.add(item)
    return c1


# 保存结果到txt文件
def save_rule(rule, save_path):
    with open(save_path, "w") as f:
        f.write("index  confidence" + "   rules\n")
        index = 1
        for item in rule:
            s = " {:<4d}  {:.3f}        {}=>{}\n".format(index, item[2], str(list(item[0])), str(list(item[1])))
            index += 1
            f.write(s)
        f.close()
    print("result saved,path is:{}".format(save_path))


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


# 根据频繁项集生成关联规则
def generate_R(dataset, min_support, min_confidence):
    L, support_data = generate_L(dataset, min_support)
    rule_list = []  # 保存满足置信度的规则
    sub_set_list = []  # 该数组保存检查过的频繁项
    for k in range(len(L)):
        for freq_set in L[k]:  # 遍历Lk
            for sub_set in sub_set_list:  # sub_set_list中保存的是L1到Lk-1
                if sub_set.issubset(freq_set):  # 检查sub_set是否是freq_set的子集
                    # 检查置信度是否满足要求，是则添加到规则
                    conf = support_data[freq_set] / support_data[freq_set - sub_set]
                    big_rule = (freq_set - sub_set, sub_set, conf)
                    if conf >= min_confidence and big_rule not in rule_list:
                        rule_list.append(big_rule)
            sub_set_list.append(freq_set)
    rule_list = sorted(rule_list, key=lambda x: x[2], reverse=True)
    return rule_list


if __name__ == '__main__':
    support_data = {}
    filename = 'apriori_plus'
    min_support = 2
    min_confidence = 0.5
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
    current_path = os.getcwd()
    if not os.path.exists(current_path + "/output"):
        os.mkdir("output")
    save_path = current_path + "/output/" + filename + ".txt"
    # L, support_data = generate_L(data_test, min_support)
    rule = generate_R(data_test, min_support, min_confidence)
    # print('L: ', L)
    # print('支持度字典：', support_data)
    print('rule: ', rule)
    save_rule(rule, save_path)
