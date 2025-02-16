from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for
from datetime import datetime
import json
import os
from app.models.Receipt import Receipt

bp = Blueprint('main', __name__, template_folder='templates')

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 处理图片上传
        file = request.files['receipt']
        if file:
            # 不保存上传的文件，而是直接获取文件内容 image_bytes
            image_bytes = file.read()
            receipt = Receipt()
            img = receipt.resize(image_bytes)
            parsed_data = receipt.recognize(img)
            # print(parsed_data)
            return render_template('edit.html', data=parsed_data)
    else:
        # 调试用，直接解析图片
        # filePath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'receipt.jpg')
        # print(filePath)
        # with open(filePath, 'rb') as f:
        #     image = f.read()
        #     receipt = Receipt()
        #     img = receipt.resize(image)
        #     # 写出调试图片
        #     with open('static/uploads/resized.jpg', 'wb') as f:
        #         f.write(img)
        #     parsed_data = receipt.recognize(img)
#             data="""{
#   "transaction_time": "2025-02-14 09:17:58",
#   "income_amount": "",
#   "expense_amount": "10.28",
#   "transaction_app": "美团App",
#   "payment_platform": "",
#   "financial_terminal": "浦发银行信用卡 (0673)",
#   "memo": "骑行套餐",
#   "category": "交通"
# }"""
#             # parsed_data = eval(data)
#             parsed_data = json.loads(data)
#             print(type(parsed_data))
            # return render_template('edit.html', data=parsed_data)
        return render_template('upload.html')

@bp.route('/save', methods=['POST'])
def save_record():
    record = {
        'platform': request.form.get('platform'),
        'amount': float(request.form.get('amount')),
        'time': datetime.strptime(request.form.get('time'), '%Y-%m-%d %H:%M:%S'),
        'location': request.form.get('location'),
        'note': request.form.get('note')
    }

    # conn = sqlite3.connect('finance.db')
    # c = conn.cursor()
    # c.execute('''INSERT INTO transactions
    #              (platform, amount, time, location, note)
    #              VALUES (?,?,?,?,?)''',
    #           (record['platform'], record['amount'],
    #            record['time'], record['location'], record['note']))
    # conn.commit()
    # conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # 如果要直接运行，可以用Flask方式
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.register_blueprint(bp)
    app.run(host='0.0.0.0', port=5000, debug=True)