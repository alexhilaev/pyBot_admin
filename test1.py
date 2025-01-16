import json

# t = [{'a': 1.0, 'b': 2.0},
#     {'a': 3.0, 'b': 4.0},
#     {'a': 5.0, 'b': 6.0},
#     {'a': 7.0, 'b': 9.0},
#     {'a': 9.0, 'b': 0.0}]
# # new_list = [i["a"] for i in t]

# x = list(map(lambda x: x["a"], t))
# print(x)

a = {'num': 1, 'data' : {'some1': 2, 'some2': 3}}
b = {'num': 2, 'data' : {'some1': 4, 'some2': 5}}
c = {'num': 42, 'data' : {'some1': 324, 'some2': 523}}
dictlist = [dict() for x in range(0)]
# jsl = [dict() for x in range(2)]

# dictlist[0] = a
# dictlist[1] = b
dictlist.append(a)
dictlist.append(b)
dictlist.append(c)


# z.update(a)
jsd = json.dumps(dictlist)
jsl = json.loads(jsd)
# print(jsd)
# print("\n")
# print(jsl)
# print("\n")
# x = (item["num"] for item in jsl)
x = list(map(lambda x: x['num'], jsl))
# print(x[-1])

for x in jsl:
    print('\nnext string:')
    print('num =', x['num'], 'data =', x['data']['some1'])
    # print('data =', x['data']['some1'])



# try:
#     for n in x:
#         print(n)
# except:
#     pass
# for x in list:
#     print(x)