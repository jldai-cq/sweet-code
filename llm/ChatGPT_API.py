import json
from openai import OpenAI
import os
from tqdm import tqdm
from datetime import datetime

now_time = datetime.now()
now = now_time.strftime("%Y%m%d%H%M")

model_name = "gpt-3.5-turbo"
# model = "gpt-4o"

os.environ["OPENAI_API_KEY"] = "sk-KGWhnKcesq6Kf5cgOUXs8rqy9xT2XUmOxH11dZuqJcvKqTAH"  # 公共 ?
# os.environ["OPENAI_API_KEY"] = "sk-Dh5lfHGAY0i0vl7YFXC0cuybShZWA4dRCPl1jB6dzlkGR6E3"   # 额度0.3

data_path = '../benchmark/subBenchmark_zs.json'
base_filename = os.path.basename(data_path)[:-5]

with open(data_path, 'r', encoding='utf-8') as f:
    datas = [json.loads(line.strip()) for line in f.readlines()]

results = []
Tokens = 0
start_index = 0
end_index = 5
tokens_list = []


# 定义保存函数
def save_results(results, tokens_list, batch_num):
    # 保存结果
    output_path = f'./output/{base_filename}_{model_name}_batch{batch_num}.json'
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')

    # 保存token信息
    tokenfile_path = f'./tokens/{base_filename}_{model_name}_batch{batch_num}_tokens.txt'
    tokenfile_dir = os.path.dirname(tokenfile_path)
    os.makedirs(tokenfile_dir, exist_ok=True)
    with open(tokenfile_path, 'w', encoding='utf-8') as file:
        for tokens in tokens_list:
            file.write(tokens + '\n')
        file.write(f"Batch {batch_num} Total Tokens: {Tokens}\n")

    print(f"Saved batch {batch_num} with {len(results)} results")


batch_size = 100
batch_num = 1

for i, item in enumerate(tqdm(datas, desc=f"{now_time} Processing data: ")):
    prompt = item['instruction']

    client = OpenAI(
        api_key=os.environ['OPENAI_API_KEY'],
        base_url="https://api.chatanywhere.tech/v1"
    )
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )

    # get token info
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens
    Tokens += total_tokens
    data_to_save = f"total_tokens: {total_tokens}, prompt_tokens: {prompt_tokens}, completion_tokens: {completion_tokens}"
    tokens_list.append(data_to_save)

    response_content = response.choices[0].message.content
    item['output'] = response_content  # 保存响应到结果中
    results.append(item)

    # 每处理100个样本保存一次
    if (i + 1) % batch_size == 0:
        save_results(results, tokens_list, batch_num)
        batch_num += 1
        # 清空结果列表，但保留总token计数
        results = []
        tokens_list = []

# 保存剩余的结果
if results:
    save_results(results, tokens_list, batch_num)

# 保存总token数统计
with open(f'./output/{base_filename}_{model_name}_total_tokens.txt', 'w', encoding='utf-8') as file:
    file.write(f"Total Tokens Used: {Tokens}\n")
