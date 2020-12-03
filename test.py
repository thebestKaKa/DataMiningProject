#encoding:utf-8
a = [1, 2]
b = [1, 2, 3, 4, 0]
c = [5, 6]
print(set(a).issubset(b))
print(set(b) - frozenset([1]))
print(set(b))
print("hello world!")