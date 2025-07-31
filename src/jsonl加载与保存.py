import json

data_path = 'results.jsonl'

# 1、加载: jsonl
with open(data_path, 'r', encoding='utf-8') as f:
    datas = [json.loads(line.strip()) for line in f.readlines()]
# 封装JSONL加载函数
def load_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line.strip()) for line in f.readlines()]

# 2、保存: jsonl
results = []
with open(data_path, 'w', encoding='utf-8') as f:
    for result in results:
        f.write(json.dumps(result, ensure_ascii=False) + '\n')


# 封装JSONL保存函数
def write_to_jsonl(path, datas):
    with open(path, 'w', encoding='utf-8') as writer:
        for data in datas:
            writer.write(json.dumps(data, ensure_ascii=False)+"\n")

# 3、合并: jsonl
data_num = 4
with open(data_path, 'w', encoding='utf-8') as f:
    for i in enumerate(range(data_num)):
        temp_file = f"data_{i}.jsonl"
        with open(temp_file, 'r', encoding='utf-8') as tf:
            f.write(tf.read())



