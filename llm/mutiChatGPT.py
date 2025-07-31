import json
import os
import time
import concurrent.futures
from tqdm import tqdm
from datetime import datetime
from openai import OpenAI
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('api_calls.log'), logging.StreamHandler()]
)

# 配置参数
model_name = "gpt-3.5-turbo"
os.environ["OPENAI_API_KEY"] = "sk-Dh5lfHGAY0i0vl7YFXC0cuybShZWA4dRCPl1jB6dzlkGR6E3"
data_path = '../benchmark/subBenchmark_zs.json'
base_filename = os.path.basename(data_path)[:-5]
now = datetime.now().strftime("%Y%m%d%H%M")

# 并发设置
MAX_WORKERS = 8  # 调整为适合CPU的并发数
BATCH_SIZE = 100  # 每批处理的样本数
MAX_RETRIES = 3  # 最大重试次数
RETRY_DELAY = 2  # 重试延迟(秒)

# 创建结果目录
results_dir = f"./results_{now}"
os.makedirs(results_dir, exist_ok=True)


# 读取数据
def load_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line.strip()) for line in f.readlines()]


# 处理单个样本
def process_item(item, client):
    prompt = item['instruction']
    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}]
            )

            # 获取token信息
            token_info = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }

            # 添加响应到结果
            result = item.copy()
            result['response'] = response.choices[0].message.content

            return result, token_info

        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                logging.warning(f"Error processing item: {str(e)}. Retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)
            else:
                logging.error(f"Failed after {MAX_RETRIES} attempts: {str(e)}")
                return item, {"error": str(e), "total_tokens": 0}

    return item, {"error": "Max retries exceeded", "total_tokens": 0}


# 处理一批数据
def process_batch(batch_items, batch_id):
    client = OpenAI(
        api_key=os.environ['OPENAI_API_KEY'],
        base_url="https://api.chatanywhere.tech/v1"
    )

    results = []
    token_infos = []
    total_tokens = 0

    # 使用线程池并发处理批次内的项目
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_item = {executor.submit(process_item, item, client): item for item in batch_items}

        for future in tqdm(concurrent.futures.as_completed(future_to_item),
                           total=len(batch_items),
                           desc=f"Batch {batch_id}"):
            result, token_info = future.result()
            results.append(result)

            if "error" not in token_info:
                token_str = f"total_tokens: {token_info['total_tokens']}, prompt_tokens: {token_info['prompt_tokens']}, completion_tokens: {token_info['completion_tokens']}"
                token_infos.append(token_str)
                total_tokens += token_info['total_tokens']
            else:
                token_infos.append(f"Error: {token_info['error']}")

    # 保存批次结果
    batch_path = os.path.join(results_dir, f"{base_filename}_{model_name}_batch{batch_id}.json")
    with open(batch_path, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')

    # 保存批次token信息
    token_path = os.path.join(results_dir, f"{base_filename}_{model_name}_batch{batch_id}_tokens.txt")
    with open(token_path, 'w', encoding='utf-8') as f:
        for token_info in token_infos:
            f.write(token_info + '\n')
        f.write(f"Batch {batch_id} Total Tokens: {total_tokens}\n")

    logging.info(f"Completed batch {batch_id}: {len(results)} items, {total_tokens} tokens")
    return total_tokens


# 主函数
def main():
    start_time = time.time()
    logging.info(f"Starting inference with model: {model_name}")

    # 加载数据
    data = load_data(data_path)
    total_items = len(data)
    logging.info(f"Loaded {total_items} items from {data_path}")

    # 分批处理
    batches = [data[i:i + BATCH_SIZE] for i in range(0, total_items, BATCH_SIZE)]
    all_results = []
    total_tokens_used = 0

    for batch_id, batch in enumerate(batches, 1):
        logging.info(f"Processing batch {batch_id}/{len(batches)}")
        batch_tokens = process_batch(batch, batch_id)
        total_tokens_used += batch_tokens

        # 合并结果
        batch_results_path = os.path.join(results_dir, f"{base_filename}_{model_name}_batch{batch_id}.json")
        with open(batch_results_path, 'r', encoding='utf-8') as f:
            batch_results = [json.loads(line) for line in f]
        all_results.extend(batch_results)

    # 保存所有结果
    final_results_path = os.path.join(results_dir, f"{base_filename}_{model_name}_all_results.json")
    with open(final_results_path, 'w', encoding='utf-8') as f:
        for result in all_results:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')

    # 保存总token信息
    total_tokens_path = os.path.join(results_dir, f"{base_filename}_{model_name}_total_tokens.txt")
    with open(total_tokens_path, 'w', encoding='utf-8') as f:
        f.write(f"Total Tokens Used: {total_tokens_used}\n")
        f.write(f"Total Items Processed: {total_items}\n")
        f.write(f"Average Tokens Per Item: {total_tokens_used / total_items if total_items else 0}\n")
        f.write(f"Total Processing Time: {time.time() - start_time:.2f} seconds\n")

    logging.info(f"Completed all processing. Total tokens: {total_tokens_used}")
    logging.info(f"Results saved to {results_dir}")


if __name__ == "__main__":
    main()
