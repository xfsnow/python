from pdfrw import PdfReader, PdfWriter

input_pdf = './PDF/Chinese.pdf'
output_pdf = './PDF/Chinese_no_watermark.pdf'
reader = PdfReader(input_pdf)
writer = PdfWriter()

for page in reader.pages:
    print(page.keys())

    # 删除每个页面的最后一个图层
    if '/CropBox' in page:
        del page['/CropBox']
    # 处理过后的页面添加到新的PDF文件中
    # print(page)
    writer.addpage(page)
    print(writer)
# 输出PDF文件
writer.write(output_pdf)