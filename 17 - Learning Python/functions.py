def function1():
    pass

def function2(test=None, fish="zebra"):
    print(test)
    print(fish)

def multi_add(*args):
    result = 0
    for i in args:
        result+= i
    return result


print(multi_add(1+100+37))

function1()