# 进行数据预处理
import warnings
import numpy as np
import csv
from efficient_apriori import apriori

warnings.filterwarnings('ignore')


lists = csv.reader(open('./groceries/groceries.csv', 'r', encoding='utf-8-sig'))
# print(lists)
data = []
for goods in lists:
    good_new = []
    for good in goods:
        if len(good):
            good_new.append(good.strip())
    # print(good_new)
    data.append(good_new)

# 挖掘频繁项集和关联规则
itemsets, rules = apriori(data, min_support=0.01, min_confidence=0.5)
print('一共有 %d 条数据' % len(data))
print('频繁项集：', itemsets)
print('关联规则：', rules)
