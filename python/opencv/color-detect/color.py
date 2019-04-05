#!/usr/bin/env python

import cv2
import numpy as np

def color_detect(image_file):
    ## Read
    img = cv2.imread(image_file)

    ## convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    ## mask of green (36,25,25) ~ (86, 255,255)
    # mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
    mask = cv2.inRange(hsv, (15, 0, 0), (36, 255,255))

    ## slice the green
    imask = mask>0
    green = np.zeros_like(img, np.uint8)
    green[imask] = img[imask]

    ## save
    cv2.imwrite("green.png", green)

if __name__ == '__main__':
    color_detect('flower.jpg')
