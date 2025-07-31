import json

data_path = 'results.json'

# 1、加载: json
with open(data_path, 'r', encoding='utf-8') as f:
    datas = [json.load(f)]


# 2、保存: json
results = []
with open(data_path,'w') as f:
    json.dump(results,f,ensure_ascii=False,indent=2)

