from openpyxl import load_workbook

str = '''看见	哪里	那边	头顶	眼睛
雪白	肚皮	孩子	天空	傍晚
人们	冬天	花朵	平常	江河
海洋	田地	工作	办法	如果
长大	四海为家	娃娃	只要
皮毛	那里	知识	花园	石桥
队旗	铜号	红领巾	欢笑
树叶	枫树	松柏	木棉	水杉
化石	金桂	写字	丛林	深处
竹林	熊猫	朋友	四季	农事
月光	辛苦	棉衣	一同	柱子
到底	秤杆	力气	出来	船身
石头	地方	果然	评奖	时间
报纸	来不及	事情	坏事
出国	好事 	今天	圆珠笔
开心	以前	还有	台灯'''

phrases = str.split()
print(phrases)


excel_template = 'pinyin_print/pinyin_square_block.xlsx'
wb = load_workbook(filename = excel_template)
ws = wb['pinyin']
pageTitle = '语文二年级上册119页汉字'
ws.title = pageTitle
d = ws.cell(row=1, column=3, value=pageTitle)
# print(ws['A1'].value)
wb.save('pinyin_print/pinyin119.xlsx')