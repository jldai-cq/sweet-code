import json

data_path = ""

# 加载: JSONL
with open(data_path, 'r', encoding='utf-8') as f:
    examples = [json.loads(line.strip()) for line in f.readlines()]


# 保存: JSONL
results = []
with open(data_path, 'w', encoding='utf-8') as f:
    for result in results:
        f.write(json.dumps(result, ensure_ascii=False) + '\n')

# 合并: JSONL
data_num = 4
with open(data_path, 'w', encoding='utf-8') as f:
    for i in range(data_num):
        temp_file = f"data_{i}.jsonl"
        with open(temp_file, 'r', encoding='utf-8') as tf:
            f.write(tf.read())
