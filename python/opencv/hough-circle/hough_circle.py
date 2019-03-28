import cv2
import numpy as np

def hough_circle(file_name):
    # 0 means gray scale image
    img = cv2.imread(file_name, 0)
    img = cv2.medianBlur(img,5)
    print("img.size: ", img.shape[0], img.shape[1])
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
                                param1=50,param2=30,minRadius=0,maxRadius=0)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        print("len(circles): ", len(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            print(i.shape)
            print(i)
            # draw the center of the circle
            cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

        cv2.imshow('detected circles',cimg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("no circle")

if __name__ == '__main__':
    #hough_circle('IMG-52.jpg')
    #hough_circle('white-fine.png')
    #hough_circle('black-fine.png')
    hough_circle('empty.png')
