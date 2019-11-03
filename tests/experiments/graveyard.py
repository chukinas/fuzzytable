class Something:

    def __init__(self, stuff):
        self.hello = stuff


allthings = [Something(i) for i in range(5)]


many = lambda x: x.hello >= 3

manythings = filter(many, allthings)


for thing in manythings:
    print(thing.hello)