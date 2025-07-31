
value = "{\"作物\": \"西瓜\"}"
print(value)    # {"作物": "西瓜"}
# 处理转义字符
value = value.replace('\\"', '"').replace("\\'", "'")
print(value)    # {"作物": "西瓜"}