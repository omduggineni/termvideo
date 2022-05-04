#!/usr/bin/env python3

import cv2
import sys
import shutil
import numpy as np
import argparse
import time

last_frame_timestamp = None

def display_frame(frame, fps=30):
    global last_frame_timestamp

    #delay based on fps using time
    if last_frame_timestamp is not None:
        delay = int(1e9/fps) - (time.time_ns() - last_frame_timestamp)
        #print(delay)
        if delay > 0:
            time.sleep(delay/1e9)
    last_frame_timestamp = time.time_ns()

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


def get_args():
    parser = argparse.ArgumentParser(description='Display video')
    parser.add_argument('video_name', type=str, help='video name')
    return parser.parse_args()

def main():
    args = get_args()
    video_name = args.video_name
    cap = cv2.VideoCapture(video_name)
    if not cap.isOpened():
        print("Error opening video stream or file")
        sys.exit(1)
    
    #get frame rate
    fps = cap.get(cv2.CAP_PROP_FPS)

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            display_frame(frame, fps)
        else:
            break

if __name__ == '__main__':
    main()