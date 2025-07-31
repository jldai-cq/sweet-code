for filename in os.listdir('.'):
    if filename.endswith('.json') or filename.endswith('.jsonl'):
        print(f"\n📂 正在处理文件：{filename}")
        split_dataset_by_task(filename)
