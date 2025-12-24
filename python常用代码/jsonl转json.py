import json

# jsonl格式的数据
jsonl_data = '''{"id": "689160a405abef89586faea3b0181e1f850469ce849ca2abfbc68f62d3f91cbc", "task": "RE", "source": "AgrRel2360K", "instruction": "{\"instruction\": \"你是专门进行关系抽取的专家。请从input中抽取出符合schema定义的关系三元组，不存在的关系返回空列表。请按照以下的JSON字符串格式回答：{'taxon rank': [{'head': '头实体', 'tail': '尾实体'}], 'subclass of': [{'head': '头实体', 'tail': '尾实体'}], 'instance of': [{'head': '头实体', 'tail': '尾实体'}], 'has part': [{'head': '头实体', 'tail': '尾实体'}], 'material used': [{'head': '头实体', 'tail': '尾实体'}]}\", \"schema\": [\"taxon rank\", \"subclass of\", \"instance of\", \"has part\", \"material used\"], \"examples\": [{\"input\": \"芦苇湿地是重要的自然湿地，在调蓄洪水、防洪排涝、净化污水，提供食物、美化环境等方面都有重要的作用。\", \"output\": \"{'has part': [], 'instance of': [], 'subclass of': [{'head': '污水', 'tail': '水'}], 'material used': [], 'taxon rank': []}\"}, {\"input\": \"西瓜病毒病主要是由花叶病毒引起的病害之一，田间表现为花叶型和蕨叶型两大类，主要危害叶片和果实，病菌依靠蚜虫等昆虫传播。\", \"output\": \"{'has part': [], 'material used': [], 'subclass of': [], 'instance of': [{'head': '西瓜', 'tail': '果实'}], 'taxon rank': []}\"}], \"input\": \"赖氨酸是一种α-氨基酸。\"}", "label": "[{\"head\": \"赖氨酸\", \"relation\": \"subclass of\", \"tail\": \"氨基酸\"}]"}
'''

# 将jsonl格式的字符串解析为json对象
json_data = json.loads(jsonl_data)

# 将解析后的json对象保存到文件
output_file = "output.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)

print(f"数据已成功保存到文件：{output_file}")