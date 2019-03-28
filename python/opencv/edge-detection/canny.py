"""
REF: https://classes.engineering.wustl.edu/ese205/core/index.php?title=OpenCV4
https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_canny/py_canny.html
"""
import cv2
import numpy as np
from matplotlib import pyplot as plt

def edge_detection(img_file_name):
    img = cv2.imread(img_file_name, 0)
    edges = cv2.Canny(img, 100, 200)
    circles = cv2.HoughCircles(edges,cv2.HOUGH_GRADIENT,1,20,
                                param1=50,param2=30,minRadius=0,maxRadius=0)

    plt.subplot(121),plt.imshow(img,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    #plt.subplot(122),plt.imshow(circles,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.show()

if __name__ == '__main__':
    edge_detection('IMG-52.jpg')
