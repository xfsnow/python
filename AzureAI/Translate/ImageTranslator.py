import datetime
import logging
import requests
import time
from PIL import Image, ImageDraw, ImageFont
import uuid
import os

# 这个脚本是一个图像翻译器，使用 Azure 的 OCR 和翻译 API 来处理图像中的文本
# 1. 它首先使用 OCR API 从图像中提取文本和边界框。
# 2. 然后，它将提取的文本批量翻译成目标语言（默认为中文）。
# 3. 最后，它将翻译后的文本绘制在原始图像上，并保存为新的图像文件。
# 4. 还可以生成一个 HTML 文件，将翻译结果覆盖在原始图像上，便于查看和进一步对比完善。
class ImageTranslator:
    def __init__(self):
        self.root_path = os.path.dirname(os.path.abspath(__file__))

        # Azure OCR API 接口，形如  https://contoso.cognitiveservices.azure.com/vision/v3.2/read/analyze
        self.ocr_endpoint = os.getenv("AZURE_OCR_ENDPOINT")
        # Azure OCR API 密钥
        self.ocr_key = os.getenv("AZURE_OCR_KEY")
        # Azure Translator API 接口，形如 https://api.cognitive.microsofttranslator.com/translate
        self.translator_endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
        # Azure Translator API 密钥
        self.translator_key = os.getenv("AZURE_TRANSLATOR_KEY")
        # Azure Translator API 区域，形如 "eastus" 或 "japanwest"
        self.translator_region = os.getenv("AZURE_TRANSLATOR_REGION")
        self.log = self.setup_logger()

    def setup_logger(self):
         # 获取子类的类名
        class_name = self.__class__.__name__
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(class_name)
        handler = logging.FileHandler(
            filename=f'{self.root_path}/{class_name}_' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.log',
            encoding='utf-8'
        )
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def ocr_image(self, image_path):
        # Read the image file
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        # Make the OCR request
        headers = {
            "Ocp-Apim-Subscription-Key": self.ocr_key,
            "Content-Type": "application/octet-stream"
        }
        response = requests.post(self.ocr_endpoint, headers=headers, data=image_data)
        response.raise_for_status()

        # Get the operation location (URL with an ID at the end)
        operation_location = response.headers["Operation-Location"]

        # Retrieve the results
        headers = {
            "Ocp-Apim-Subscription-Key": self.ocr_key
        }
        result_response = requests.get(operation_location, headers=headers)
        result_response.raise_for_status()
        result = result_response.json()
        # OCR是异步操作，这里需要添加一个循环来等待结果
        while ("status" in result) and (result["status"] != "succeeded"):
            self.log.debug(result)
            time.sleep(1)
            result_response = requests.get(operation_location, headers=headers)
            result_response.raise_for_status()
            result = result_response.json()
        # Extract text and bounding boxes
        text_data = []
        for read_result in result["analyzeResult"]["readResults"]:
            for line in read_result["lines"]:
                text_data.append({
                    "text": line["text"],
                    "bounding_box": line["boundingBox"]
                })

        return text_data

    # 单行文字单语种快速翻译
    def translate(self, text, target_language="zh-Hans"):
        body = [{'text': text}]
        results = self.translate_batch(body, target_language=[target_language])
        translated_text = results[0]["translations"][0]["text"]
        return translated_text

    # 批量翻译
    def translate_batch(self, body, target_language=["zh-Hans"]):
        params = {
            'api-version': '3.0',
            'from': 'en',
            'to': target_language
        }
        headers = {
            'Ocp-Apim-Subscription-Key': self.translator_key,
            'Ocp-Apim-Subscription-Region': self.translator_region,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }
        # self.log.debug(body)

        # Send batch translation request
        response = requests.post(self.translator_endpoint, params=params, headers=headers, json=body)
        response.raise_for_status()
        translations = response.json()
        return translations

    def draw_translated_text(self, image_path, text_data):
        # Open the image
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        # 加载一个中文字体，以便支持中文字符
        font = ImageFont.truetype("RoyalCheese.ttf", size=20)

        # Draw each translated text at the original position
        for item in text_data:
            text = item["translated_text"]
            # 如果 text 是空字符串、纯英文或数字，则跳过不画
            if all(c.isascii() for c in text) or text == "":
                continue
            bounding_box = item["bounding_box"]
            draw.text((bounding_box[0], bounding_box[1]), text, font=font, fill=(0, 0, 0))

        # 把翻译后的图片保存为 jpg 格式，调试期间文件名以时间戳命名
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        image.save(f"translated_image_{timestamp}.jpg")

    def make_html(self,image_path, text_data):
        # 生成 HTML 文件，先把原画放在背景上，用 CSS 绝对定位
        # 然后把翻译结果画在上面
        html_content = '''<!DOCTYPE html>
<html lang="zh-cn">
<head>
<meta charset="utf-8" />
<link href='translate.css' rel='stylesheet' type='text/css'/>
<title>'''+image_path+'''</title>
</head>
<body>'''
        html_content += f'<img src="{image_path}" style="position:absolute; top:0; left:0;">'
        for item in text_data:
            text = item["translated_text"]
            # 如果 text 是空字符串、纯英文或数字，则跳过不画。但是包含“DailyDoseOfDS.com”的不跳过，而是把内容替换成“www.snowpeak.org”
            if text == "join.DailyDoseOfDS.com":
                text = "www.snowpeak.org"
            elif all(c.isascii() for c in text) or text == "鲁":
                continue
            bounding_box = item["bounding_box"]
            # Azure AI Vision 返回的 bounding box（边界框）通常是一个包含 8 个数字的数组，用于描述图像中检测到的对象的四个角点坐标。它的格式如下：[x1, y1, x2, y2, x3, y3, x4, y4]
            # 这种格式支持 任意四边形，可以更准确地表示倾斜或旋转的对象，尤其适用于文档分析、OCR（光学字符识别）等场景。
            x_coords = bounding_box[0::2]  # 提取 x 坐标 [x1, x2, x3, x4]
            y_coords = bounding_box[1::2]  # 提取 y 坐标 [y1, y2, y3, y4]
            left = min(x_coords)  # 左边界
            top = min(y_coords)  # 上边界
            width = max(x_coords) - left  # 宽度
            height = max(y_coords) - top  # 高度
            fontSize=''
            if width > 400:
                # 根据文本框宽度和文字字数计算字号大小，如果框宽，但字少，则加大字号
                font_size = max(12, int(width / (len(text))))  # 字号大小
                fontSize=f'font-size:{font_size}px;'

            # 使用绝对定位将文本放置在正确的位置
            html_content += f'<div style="left:{left}px; top:{top}px; width:{width}px; height:{height}px; {fontSize}">{text}</div>'
        html_content += "</body></html>"

        # 保存 HTML 文件
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        with open(f"{self.root_path}/trans_{timestamp}.html", "w", encoding="utf-8") as f:
            f.write(html_content)

    def process_image(self, image_path):
        # 1: OCR 提取文本及边界框
        text_data = self.ocr_image(image_path)

        # 2: 所有文本组织到一起，一次性调用翻译接口翻译成中文
        texts_to_translate = [item["text"] for item in text_data]
        body = [{'text': text} for text in texts_to_translate]
        # self.log.debug(body)
        translations = self.translate_batch(body, target_language=["zh-Hans"])
        # 把翻译结果放回到原来的位置
        for item, translation in zip(text_data, translations):
            item["translated_text"] = translation["translations"][0]["text"]
        # self.log.debug(text_data)
        # 3: 把翻译结果画到原图上
        # self.draw_translated_text(image_path, text_data)
        self.make_html(image_path, text_data)

if __name__ == "__main__":
#     input = '''Thank you for taking the time to submit your application for Account Technology Strategist (Job number: 1823303)! We’re glad you value your career at Microsoft and we're here to help you find your next great fit as you continue your journey with us.

# What to expect in the internal hiring process
# To learn more about our hiring process, please visit the Careers Site and navigate to 'How we hire' in the top navigation menu.

# As your application progresses through the process, updates can be viewed through your Action Center. If you see the job moved to an archived state, that means the position is either no longer open, you withdrew from consideration, or you were not selected for the role.

# How’s your profile?
# A key part of the review process is evaluating your profile in relation to the job requirements, so please make sure your profile is accurate and extensive – it’s our first step in getting to know you. You can build your profile any way you’d like – you can import it from LinkedIn, manually update it, or import/attach a resume. The most important thing is that your profile tells your story!

# Key points to remember
# •	If this role change results in a different level, business group, profession, discipline, or location than that of your current role, there may be adjustments to your compensation. Watch this short 'Understanding Compensation' video series to learn more.
# •	Learn more about our internal movement philosophy such as manager notification, transfer eligibility, and transition timelines.
# •	Informationals are not part of the hiring process. Rather, they are a valuable networking tool and key element of career planning to help you proactively identify what your next role could be when you are ready to take that next step. Learn more about informational guidance for employees.
# We encourage you to check back frequently and continue to look for opportunities that match your interests, as new jobs are being posted regularly.
# '''
#     output = translator.translate(input, target_language="zh-Hans")
#     print(output)

    # Create an instance of ImageTranslator
    # translator = ImageTranslator(ocr_endpoint, ocr_key, translator_endpoint, translator_key, translator_region)
    translator = ImageTranslator()
    # Provide the path to the image file
    image_path = translator.root_path + "/local_mcp.jpg"
    translator.process_image(image_path)
