import json
import os

file_path = 'benchmark_zs_RE.jsonl'
base_name = os.path.splitext(file_path)[0]
print(base_name)

with open(file_path, 'r', encoding='utf-8') as fin:
    for line in fin:
        data = json.loads(line.strip())
        source = data.get('source', None)