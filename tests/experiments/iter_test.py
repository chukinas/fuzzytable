class MyDict:

    def __init__(self):
        self.d = {
            'hello': 'goodbye',
            3: 1245,
        }
        self.d.get(3, )

    def __iter__(self):
        yield from self.d

    def keys(self):
        return (key for key in self)


mydict = MyDict()
for c in mydict:
    print(c)

print("\nkeys:")
for key in mydict.keys():
    print(key)

print(3 in mydict)

