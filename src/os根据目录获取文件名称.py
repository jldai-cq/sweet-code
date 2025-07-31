import os

predictions_file = './output/benckmark_ft_qwen3_8b_base.jsonl'

predictions_dir = os.path.dirname(predictions_file)  # ./output
os.makedirs(predictions_dir, exist_ok=True)     # 检查./output目录是否存在，不存在则创建

predictions_filename = os.path.basename(predictions_file)  # benckmark_ft_qwen3_8b_base.jsonl
# 去掉 .jsonl 后缀
if predictions_filename.endswith('.jsonl'):
    base_filename = predictions_filename[:-6]  # benckmark_ft_qwen3_8b_base
else:
    base_filename = predictions_filename

print(f"data_name: {base_filename}")