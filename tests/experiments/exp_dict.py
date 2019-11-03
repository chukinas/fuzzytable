
a = {'a': 1, 'b': 2}
b = a
del b['a']

print(a)
print(b)

c = 5
del a
del b, c
