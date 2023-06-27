# read a local mp4 video file input.mp4,
# watermark area: starting point coordinate(52, 634), width 176, height 56
# remove the watermark by bluring the watermark area instead of cropping 
# and save it as a new mp4 video file， out.mp4

import cv2
import time

input_file_path='input.mp4'
input_file_path=  r'C:\Users\xuefe\Videos\Video\009.声音从哪生出来_n4JEtZY1Ros.mp4'
output_file_path='out.mp4'
# read the input video file
cap = cv2.VideoCapture(input_file_path)
# get the video fps, width, height
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# get the video codec
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# create VideoWriter object
out = cv2.VideoWriter(output_file_path, fourcc, fps, (width, height))

# output a progress bar in log terminal
while True:
    # read the next frame
    ret, frame = cap.read()
    if ret:
        # get the watermark area
        watermark_area = frame[634:634+56, 52:52+176]
        # 把水印区域用黑色框线标出
        # cv2.rectangle(frame, (52, 634), (52+176, 634+56), (0, 0, 0), 2)
     
        # paint the watermark area with colors that around the watermark area

        # get the colors of the four corners of the watermark area
        # top left corner
        top_left_corner = frame[634, 52]
        # top right corner
        top_right_corner = frame[634, 52+176-1]
        # bottom left corner
        bottom_left_corner = frame[634+56-1, 52]
        # bottom right corner
        bottom_right_corner = frame[634+56-1, 52+176-1]

        # TODO: 用四个角的颜色向中心点的颜色渐变填充，效果也许会更好
        # 水印区域左上四分之一使用左上角的颜色填充
        frame[634:634+28, 52:52+88] = top_left_corner
        # 水印区域右上四分之一使用右上角的颜色填充
        frame[634:634+28, 52+88:52+176] = top_right_corner
        # 水印区域左下四分之一使用左下角的颜色填充
        frame[634+28:634+56, 52:52+88] = bottom_left_corner
        # 水印区域右下四分之一使用右下角的颜色填充
        frame[634+28:634+56, 52+88:52+176] = bottom_right_corner

        # write the frame to the output video file
        out.write(frame)
    else:
        break
    
    # start = time.perf_counter()
    # for i in range(scale + 1):
    #     a = "*" * i
    #     b = "." * (scale - i)
    #     c = (i / scale) * 100
    #     dur = time.perf_counter() - start
    #     print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c,a,b,dur),end = "")
    #     time.sleep(0.1)
    # print("\n"+"执行结束，万幸".center(scale // 2,"-"))

# release the VideoCapture object
cap.release()
# release the VideoWriter object
out.release()
# close all windows
cv2.destroyAllWindows()

