import cv2
import sys
import shutil
import numpy as np
from time import sleep

video_name = sys.argv[1]
cap = cv2.VideoCapture(video_name)

chars = " .,:;i1tfLCG08@"

def display_frame(frame):
    #get terminal size
    columns, rows = shutil.get_terminal_size()
    #resize frame to fit terminal
    frame = cv2.resize(frame, (columns-1, rows), cv2.INTER_AREA)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #clear terminal color
    for row in np.arange(rows):
        for col in np.arange(columns-1):
            #get pixel value
            pixel = frame[row][col]
            #convert to ascii
            #ascii_value = chars[int(pixel[0]/255 * (len(chars)-1))]
            #go to row and col using escape
            sys.stdout.write("\033[{};{}H".format(row, col))
            #truecolor code
            sys.stdout.write("\033[48;2;{};{};{}m".format(pixel[0], pixel[1], pixel[2]))
            #print to terminal
            sys.stdout.write(" ")

# image = cv2.imread("ppmSample.ppm")
# display_frame(image)
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        display_frame(frame)
    else:
        break

# sys.stdout.write("\x1b[48;2;{};{};{}m".format(0, 0, 0))