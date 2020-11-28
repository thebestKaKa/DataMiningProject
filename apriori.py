#encoding:utf-8
import csv

def apriori(data, min_support, min_confidence):
    frequent_item_sets = {}





lists = csv.reader(open('./groceries/groceries.csv', 'r', encoding='utf-8-sig'))
# print(lists)
data = []
for goods in lists:
    good_new = []
    for good in goods:
        if len(good):
            good_new.append(good.strip())
    data.append(good_new)

