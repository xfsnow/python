from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for
import os
from datetime import datetime
from app.models.Receipt import Receipt

bp = Blueprint('main', __name__, template_folder='templates')

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 处理图片上传
        file = request.files['receipt']
        if file:
            ext = os.path.splitext(file.filename)[1]
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
            # 使用 current_app.config 而不是 bp.config
            strUploadFolder = current_app.config['UPLOAD_FOLDER']
            filepath = os.path.join(strUploadFolder, filename)
            file.save(filepath)

            # GPT-4o识别文字
            with open(filepath, 'rb') as f:
                image = f.read()



            # 解析关键信息（示例解析逻辑）
            parsed_data = {
                'img_url': filename,
                'platform': '微信支付',
                'amount': '',
                'time': 'time',
                'location': 'location',
                'note': '备注'
            }
            return render_template('edit.html',
                                 data=parsed_data)
    else:
        # 调试用，直接解析图片
        # filePath = os.path.join(current_app.config['UPLOAD_FOLDER'], '20250215170459.jpg')
        # print(filePath)
        # with open(filePath, 'rb') as f:
        #     image = f.read()
        #     receipt = Receipt()
        #     parsed_data = receipt.recognize(image)
            # print(parsed_data)
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