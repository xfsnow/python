import datetime
import logging
import requests
import time
from PIL import Image
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
        self.term_set = None

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
            filename=f'{self.root_path}/{class_name}_' + self.timestamp() + '.log',
            encoding='utf-8'
        )
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def timestamp(self):
        # 获取当前时间戳
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        return timestamp

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

    def make_html(self, image_path, text_data):
        timestamp = self.timestamp()
        image_file = os.path.basename(image_path)
        # 先复制一份原图用于擦除
        image = Image.open(image_path).convert("RGB")
        # draw = ImageDraw.Draw(image)
        # erased_img_name = f"{self.root_path}/{image_file}_erased_{timestamp}.jpg"
        # 生成 HTML 文件，底层图片用擦除后的图片
        html_content = '''<!DOCTYPE html>
<html lang="zh-cn">
<head>
<meta charset="utf-8" />
<link href='translate.css' rel='stylesheet' type='text/css'/>
<title>''' + image_file + '''</title>
</head>
<body>'''
        html_content += f'<img src="{image_file}" style="position:absolute; top:0; left:0;">'
        # 合并循环：只对需要显示中文的区域填色并生成div
        for item in text_data:
            text_eng = item["text"]
            text = item["translated_text"]
            show_text = None
            if "doseofds.com" in text.lower():
                show_text = "www.snowpeak.org"
            elif text.isascii() or text == "鲁" or self.is_term(text_eng):
                continue
            else:
                show_text = text
            bounding_box = item["bounding_box"]
            x_coords = bounding_box[0::2]
            y_coords = bounding_box[1::2]
            left = min(x_coords)
            top = min(y_coords)
            right = max(x_coords)
            bottom = max(y_coords)
            width = right - left
            height = bottom - top
            # 取左上角像素做背景色
            original_color = image.getpixel((int(left), int(top)))
            # 把背景色转换成CSS颜色格式 background-color: rgba(255, 255, 255, 1);
            background_color = f'rgba({original_color[0]}, {original_color[1]}, {original_color[2]}, 1)'
            # 字号
            fontSize = f'font-size:{height}px;'
            # if width > 400:
            #     font_size = max(12, int(width / (len(show_text))))
            #     fontSize = f'font-size:{font_size}px;'
            # 生成div
            html_content += f'<div style="left:{left}px; top:{top}px; width:{width}px; height:{height}px;{fontSize} background-color: {background_color};">{show_text}</div>\n'
        html_content += "</body></html>"

        # 保存 HTML 文件
        with open(f"{self.root_path}/{image_file}_{timestamp}.html", "w", encoding="utf-8") as f:
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
        self.make_html(image_path, text_data)

    def is_term(self, text):
        # 首次调用时读取术语表并缓存
        if self.term_set is None:
            self.term_set = set()
            with open(f"{self.root_path}/terminology.csv", "r", encoding="utf-8") as file:
                for line in file:
                    term = line.strip().split(",")[0]
                    self.term_set.add(term)
        return text in self.term_set


if __name__ == "__main__":
    translator = ImageTranslator()
    # text = 'lamaIndex'
    # is_term = translator.is_term(text)
    # print(f"Is '{text}' a term? {is_term}")

    # OCR 不支持gif格式的图片
    # 循环 01.png 到 09.png 处理
    for i in range(1, 10):
        image_file = f"0{i}.png"
        image_path = translator.root_path + "/" + image_file
        translator.process_image(image_path)
        # 休息 5秒，避免触发 Azure 的速率限制
        # time.sleep(5)
    # image_file ='03.jpg'
    # image_path = translator.root_path + "/" + image_file
    # translator.process_image(image_path)
