import json

# 1. list
data = [{"name": "代"}]
print(f"type: {type(data)}")
print(f"data: {data}")
print(f"\n")

# 2. json str
data = json.dumps(data, ensure_ascii=False)
print(f"type: {type(data)}")
print(f"data: {data}")
print(f"\n")

# 3. json str -> list
data = json.loads(data)
print(f"type: {type(data)}")
print(f"data: {data}")

"""
type: <class 'list'>
data: [{'name': '代'}]

type: <class 'str'>
data: [{"name": "代"}]

type: <class 'list'>
data: [{'name': '代'}]
"""