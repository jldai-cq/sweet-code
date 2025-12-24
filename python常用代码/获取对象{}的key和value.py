import json

# data = "{\n  \"属于\": [\n    {\n      \"head\": \"蚕豆\",\n      \"tail\": \"荚果\"\n    }\n  ],\n  \"具有\": [\n    {\n      \"head\": \"蚕豆\",\n      \"tail\": \"种子\"\n    }\n  ]\n}"
data = "{\n  \"属于\": [\n    {\n      \"head\": \"蚕豆\",\n      \"tail\": \"荚果\"\n    }\n  ],\n  \"具有\": []\n}"
data = json.loads(data)

new_record = []
for key, values in data.items():
    print("key: ", key)      # relation
    print("values: ", values, type(values))       # triples

    for iit in values:
        print("iit: ", iit, type(iit))
        iit = json.dumps(iit, ensure_ascii=False)
        iit = json.loads(iit)
        print(iit, type(iit))      # triple
        head = iit.get('head', '')
        tail = iit.get('tail', '')
        print(head)
        print(tail)
        new_record.append((head, key, tail))

print(new_record)

"""
key:  属于
values:  [{'head': '蚕豆', 'tail': '荚果'}] <class 'list'>
iit:  {'head': '蚕豆', 'tail': '荚果'} <class 'dict'>
{'head': '蚕豆', 'tail': '荚果'} <class 'dict'>
蚕豆
荚果
key:  具有
values:  [{'head': '蚕豆', 'tail': '种子'}] <class 'list'>
iit:  {'head': '蚕豆', 'tail': '种子'} <class 'dict'>
{'head': '蚕豆', 'tail': '种子'} <class 'dict'>
蚕豆
种子
[('蚕豆', '属于', '荚果'), ('蚕豆', '具有', '种子')]
"""