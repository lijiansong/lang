import cv2
import numpy as np

def harris_corner(filename):
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)

    # result is dilated for marking the corners, not important
    dst = cv2.dilate(dst, None)
    print(dst.shape)
    # Threshold for an optimal value, it may vary depending on the image.
    print(dst > 0.01 * dst.max())
    img[dst > 0.01 * dst.max()] = [0, 0, 255]

    cv2.imshow('dst', img)
    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()

if __name__ == '__main__':
    #harris_corner('IMG-52.jpg')
    harris_corner('IMG-111.jpg')
