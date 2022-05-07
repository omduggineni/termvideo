#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import sys
import shutil
import numpy as np
import argparse
import time
import os
import atexit

last_frame_timestamp = None

def hide_cursor():
    #tput civis
    os.system('tput civis')

def show_cursor():
    #tput cnorm
    os.system('tput cnorm')

def clear_screen():
    #clear screen
    sys.stdout.write("\033[2J")

def display_frame_truecolor(frame, fps=30):
    global last_frame_timestamp

    #delay based on fps using time
    if last_frame_timestamp is not None:
        delay = int(1e9/fps) - (time.time_ns() - last_frame_timestamp)
        #print(delay)
        if delay > 0:
            time.sleep(delay/1e9)
    last_frame_timestamp = time.time_ns()

    rows = frame.shape[0]
    cols = frame.shape[1]

    #go to row 0 col 0 in terminal
    sys.stdout.write("\033[0;0H")
    for row in range(rows):
        for col in range(cols):
            #get pixel value
            pixel = frame[row][col]
            #convert to ascii
            #ascii_value = chars[int(pixel[0]/255 * (len(chars)-1))]
            #truecolor code
            sys.stdout.write(f"\033[48;2;{pixel[2]};{pixel[1]};{pixel[0]}m ")
        #go to next line
        sys.stdout.write("\n")


ascii_chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]
#ansi_block_chars = " ░▒▓█"
num_ascii_chars = len(ascii_chars)

def display_frame_w_charset(frame, fps=30, charset=ascii_chars):
    global last_frame_timestamp
    len_charset = len(charset)

    #delay based on fps using time
    if last_frame_timestamp is not None:
        delay = int(1e9/fps) - (time.time_ns() - last_frame_timestamp)
        #print(delay)
        if delay > 0:
            time.sleep(delay/1e9)
    last_frame_timestamp = time.time_ns()

    rows = frame.shape[0]
    cols = frame.shape[1]

    #go to row 0 col 0 in terminal
    sys.stdout.write("\033[0;0H")

    for row in range(rows):
        for col in range(cols):
            #get pixel value
            pixel = frame[row][col]
            #convert to ascii
            char_val = charset[int(pixel[0]/255 * (len_charset-1))]
            sys.stdout.write(char_val)
        #go to next line
        sys.stdout.write("\n")

def resize_to_terminal(frame):
    columns, rows = shutil.get_terminal_size()
    return cv2.resize(frame, (columns, rows-1), cv2.INTER_AREA)

render_backends = {
    "ascii": lambda frame,fps:display_frame_w_charset(frame, fps=fps, charset=ascii_chars),
    # "ansi": lambda frame,fps:display_frame_w_charset(frame, fps=fps, charset=ansi_block_chars),
    "truecolor": display_frame_truecolor
}

def get_args():
    parser = argparse.ArgumentParser(description='Display video')
    parser.add_argument('video_name', type=str, help='video name')
    parser.add_argument('-b', '--render_backend', type=str, help='What characters to render the video with. Options: \"ascii\" (ascii characters), \"truecolor\" (truecolor escape sequences)', default="truecolor", choices=["ascii", "ansi", "truecolor"])
    return parser.parse_args()

def main():
    #hide cursor, show cursor at exit
    hide_cursor()
    atexit.register(show_cursor)
    atexit.register(clear_screen)

    #parse args
    args = get_args()
    video_name = args.video_name
    render_backend = args.render_backend
    if render_backend not in render_backends: 
        print(f"ERROR: Invalid render backend: {render_backend}", file=sys.stderr)
        sys.exit(1)
    else:
        render_backend = render_backends[render_backend]
    
    cap = cv2.VideoCapture(video_name)
    if not cap.isOpened():
        print("Error opening video stream or file")
        sys.exit(1)
    
    #get frame rate
    fps = cap.get(cv2.CAP_PROP_FPS)

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            #resize to terminal
            frame = resize_to_terminal(frame)
            #display frame
            render_backend(frame, fps)
        else:
            break

if __name__ == '__main__':
    main()