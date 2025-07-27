import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

# 从环境变量中获取API密钥和基础URL
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model_name = os.getenv("OPENAI_MODEL_NAME", "deepseek-reasoner")  # 默认模型

# 检查必要的环境变量是否存在
if not api_key:
    raise ValueError("未找到OPENAI_API_KEY环境变量，请在.env文件中设置")
if not base_url:
    raise ValueError("未找到OPENAI_BASE_URL环境变量，请在.env文件中设置")

# 初始化OpenAI客户端
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

def send_request(prompt):
    print(f"🔄 使用模型: {model_name}")
    print(f"🔄 使用API: {base_url}")

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model_name,
            stream=False
        )

        # 添加异常处理
        try:
            reasoning_content = chat_completion.choices[0].message.reasoning_content
        except AttributeError as e:
            print(f'⚠️ 获取 reasoning_content 时出错: {e}')
            reasoning_content = None

        return chat_completion.choices[0].message.content, reasoning_content

    except Exception as e:
        print(f"❌ 发送请求时出错: {e}")
        return f"错误: {str(e)}", None
