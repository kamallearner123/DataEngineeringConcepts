

# Context managers

# fd = open("sample.py")
# data = fd.read()
# print(data)
# fd.close()

with open("sample.py") as fd:
    print(dir(fd))
    data = fd.read()
    print(data)

print("End!!!!")