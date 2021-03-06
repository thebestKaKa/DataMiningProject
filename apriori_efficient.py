# 进行数据预处理
import csv
import warnings

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
    data.append(good_new)

# 调库挖掘频繁项集和关联规则
item_sets, rules = apriori(data, min_support=0.01, min_confidence=0.5)
print('一共有 %d 条数据' % len(data))
print('频繁项集：', item_sets)
print('关联规则：', rules)