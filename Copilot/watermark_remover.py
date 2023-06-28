# read a local mp4 video file input.mp4,
# watermark area: starting point coordinate(52, 634), width 176, height 56
# remove the watermark by bluring the watermark area instead of cropping 
# and save it as a new mp4 video file， out.mp4

import cv2
from moviepy.editor import VideoFileClip
import time

input_file_path='input.mp4'
input_file_path=  r'C:\Users\xuefe\Videos\Video\009.声音从哪生出来_n4JEtZY1Ros.mp4'
output_file_path='output.mp4'

def overwrite_watermark(frame, top_x, top_y, width, height):
    # Define the watermark area
    watermark_area = frame[top_y:top_y+height, top_x:top_x+width]

    # Get the colors of the four corners of the watermark area
    # top left corner
    top_left_corner = frame[top_y, top_x]
    # top right corner
    top_right_corner = frame[top_y, top_x+width-1]
    # bottom left corner
    bottom_left_corner = frame[top_y+height-1, top_x]
    # bottom right corner
    bottom_right_corner = frame[top_y+height-1, top_x+width-1]

    # Overwrite the watermark area with colors that around the watermark area
    # top left quarter of the watermark area
    frame[top_y:top_y+height//2, top_x:top_x+width//2] = top_left_corner
    # top right quarter of the watermark area
    frame[top_y:top_y+height//2, top_x+width//2:top_x+width] = top_right_corner
    # bottom left quarter of the watermark area
    frame[top_y+height//2:top_y+height, top_x:top_x+width//2] = bottom_left_corner
    # bottom right quarter of the watermark area
    frame[top_y+height//2:top_y+height, top_x+width//2:top_x+width] = bottom_right_corner

    return frame


# original audio sound should be reserved to output file directly.

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
        frame = overwrite_watermark(frame, 52, 634, 176, 56)
        frame = overwrite_watermark(frame, 1150, 4, 126, 45)
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

# Load the video file
input_video = VideoFileClip(input_file_path)
# 提取音频
audio = input_video.audio

output_video = VideoFileClip(output_file_path)
output_video = output_video.set_audio(input_video.audio)

output_video.write_videofile('out.mp4')
