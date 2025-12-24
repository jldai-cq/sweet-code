import json
def load_data(path):
    """加载 JSONL 文件数据"""
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line.strip()) for line in f.readlines()]

data_path = 'benchmark_ft_qwen3_8b_RE.jsonl'
output_path = 'benchmark_ft_qwen3_8b_RE_fixed.jsonl'
datas = load_data(data_path)

with open(output_path, 'w', encoding='utf-8') as f_out:
    for data in datas:
        # 创建数据副本，避免修改原始数据
        processed_data = data.copy()
        output_str = processed_data['output']