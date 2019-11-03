

def numgen(last_num):
    num = 1
    going = True
    while going:
        yield num
        num += 1
        if num > last_num:
            going = False


for num in numgen(3):
    print(num)


def numgen2(last_num):
    num = 1
    while True:
        yield num
        num += 1
        if num > last_num:
            return



for num in numgen2(3):
    print(num)
