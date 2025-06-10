import requests
import json
import re 

# 设置 Ollama 本地 API 地址
OLLAMA_URL = "http://localhost:11434/api/generate"

# 发送的提示词（你可以自由更改）
prompt_text = "你好，请用一句话介绍你自己。"

# 构造请求体
payload = {
    "model": "deepseek-r1:1.5b",  # 使用你本地部署的模型名
    "prompt": prompt_text,
    "stream": True  # 流式返回，每段是一行 JSON
}

def clean_response(text: str) -> str:
    # 清除所有 <think>...</think> 及其内容
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

response = requests.post(OLLAMA_URL, json=payload, stream=True)

if response.status_code == 200:
    all_raw = ""
    # print("🤖 AI 原始回应片段（含 <think>）：")
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    all_raw += data["response"]
                    print(data["response"], end="", flush=True)
            except Exception as e:
                print("\n❌ JSON 解码失败：", e)

    # print("\n\n🧼 清洗后的输出：")
    final_text = clean_response(all_raw)
    print(final_text.strip())
else:
    print(f"❌ 请求失败：{response.status_code}")
    print(response.text)