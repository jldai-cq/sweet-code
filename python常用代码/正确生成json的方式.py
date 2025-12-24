# 正确生成 JSON 的方式
import json

data = {
    "危害": [{"head": "蚕豆", "tail": "乳白、资、褐或青色种皮"}]
}
json_str = json.dumps(data, ensure_ascii=False)

print(json_str)