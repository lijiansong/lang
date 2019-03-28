#!/usr/bin/env python
import cv2
import numpy as np
from matplotlib import pyplot as plt

def trans(img_file_name):
    img = cv2.imread(img_file_name)
    rows, cols, ch = img.shape
    print(rows, cols, ch)

    pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
    pts2 = np.float32([[0,0],[cols, 0],[0, rows],[cols, rows]])

    M = cv2.getPerspectiveTransform(pts1,pts2)

    dst = cv2.warpPerspective(img,M,(cols, rows))

    plt.subplot(121),plt.imshow(img),plt.title('Input')
    plt.subplot(122),plt.imshow(dst),plt.title('Output')
    plt.show()

if __name__ == '__main__':
    trans('IMG-52.jpg')
