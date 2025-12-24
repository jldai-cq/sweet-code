

def extract_json_content(text):
    # 处理换行符和空格
    cleaned_text = text.replace('\n', ' ').strip()

    start_index = cleaned_text.find('{')
    end_index = cleaned_text.rfind('}')

    if start_index != -1 and end_index != -1 and end_index > start_index:
        return cleaned_text[start_index:end_index + 1]
    else:
        return text