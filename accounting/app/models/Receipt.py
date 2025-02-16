# filepath: /c:/Study/GitHub/python/accounting/app/models/ai.py
import os
import base64
import json
import openai

# 在环境变量或配置中设置以下参数：
#   AZURE_API_KEY        Azure OpenAI 的API密钥
#   AZURE_API_ENDPOINT   Azure OpenAI 的API端点，比如 https://xxx.openai.azure.com/
#   AZURE_API_VERSION    Azure OpenAI API版本号，比如 2024-08-01-preview
#   AZURE_MODEL_NAME     GPT-4o部署的模型名称

openai.azure_endpoint = os.getenv("AZURE_API_ENDPOINT", "")
openai.api_key = os.getenv("AZURE_API_KEY", "")
openai.api_type = "azure"
openai.api_version = os.getenv("AZURE_API_VERSION", "2024-08-01-preview")
openai.model = os.getenv("AZURE_MODEL_NAME", "gpt-4o")

class Receipt:
    """
    用于连接 Azure OpenAI GPT-4o 模型并解析收支截图。
    """
    # def __init__(self, model=None):
    #     self.model = model or MODEL_NAME

    # 注意传图片体积太大时API会报错 {'error': {'code': '429', 'message': 'Rate limit is exceeded. Try again in 86400 seconds.'}}
    # 虽说文档说文体体积最大512MB，实际200多KB的图片都会报错。换成小点的图片。
    # 识别图片内容
    def recognize(self, image_bytes: bytes) -> dict:
        # 将图片转为base64供GPT-4o分析（如功能受限可使用OCR再传文本）
        img_type = "image/jpeg"
        b64_image = base64.b64encode(image_bytes).decode("utf-8")

        # prompt = "这是交易截图的base64编码，请识别消费/收入信息，并返回 JSON 格式:" + b64_image + """
        prompt = """
这是交易截图的base64编码，请识别消费/收入信息，并返回 JSON 格式:
提取字段:
交易时间：如2025-02-15 12:30:00，使用时间格式表示
收入金额：如99.99，使用数字表示，如果没有收入则为空
支出金额：如99.99，使用数字表示，如果没有支出则为空
消费的应用：如拼多多、线下商店、公交473路等
支付平台：如微信、支付宝、美团支付等
金融终端：如某银行银行卡、信用卡、微信零钱，支付宝花呗等
说明：如小票备注、商品名称、交易号等
类别：如餐饮、交通、购物、医疗等

返回示例格式:
{
  "transaction_time": "2025-02-15 12:30:00",
  "income_amount": "",
  "expense_amount": "99.99",
  "consumption_app": "Pinduoduo",
  "payment_platform": "WeChat",
  "financial_terminal": "Credit Card",
  "notes": "Order ID: 987654321",
  "category": "dining"
}
如果无法识别，返回空。
"""
        jsonMessages = [
                {
                    "role": "system",
                    "content": "你是一个善于结构化信息提取的助手。"
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{img_type};base64,{b64_image}"},
                        },
                    ],
                }
            ]
        completion = openai.chat.completions.create(model=openai.model, messages=jsonMessages)
        jsonResponse = completion.to_json()
        # 返回的 content 写出成文件，方便查看内容，以及提取出有用的信息
        # with open("response.json", "w", encoding="utf-8") as f:
        #     f.write(jsonResponse)

        # 先把字符串 jsonResponse 转换成Python字典
        parsed_response = json.loads(jsonResponse)

        #  message.content。如果存在 ["choices"][0]["message"]["content"] 则继续，否则返回失败提示信息
        if "choices" not in parsed_response or len(parsed_response["choices"]) == 0:
            return {"error": "No response from GPT-4o."}

        jsonContent = parsed_response["choices"][0]["message"]["content"]
        return jsonContent