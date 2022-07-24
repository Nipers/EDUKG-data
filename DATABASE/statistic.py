file = open("datatolink.txt", "r", encoding="utf-8")
info = {}
for line in file:
    line = line.strip()[1:-1]
    ls = line.split(", ")
    for item in ls:
        t = item.split(": ")
        # print(t)
        a = int(t[0])
        b = int(t[1])
        if info.get(b) == None:
            info[b] = 0
        info[b] += 1
array = []
for key in info:
    array.append((key, info[key]))
def take(elem):
    return elem[0]
array.sort(key=take)
for item in array:
    print(item)
    