from flask import Flask, render_template

app = Flask(__name__)

@app.route('/learn')
def show_learn():
    # 将 title 和 name 变量传递给 learn.html 模板
    data = {
        "transaction_time": "2025-02-14 09:17:58",
        "income_amount": "",
        "expense_amount": "10.28",
        "transaction_app": "美团App",
        "payment_platform": "",
        "financial_terminal": "浦发银行信用卡(0673)",
        "memo": "骑行套餐",
        "category": "交通"
    }
    # 输出 data 的类型
    print(type(data))

    # return render_template('learn.html', data=data)
    return render_template('edit.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)