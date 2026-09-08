import cv2 as cv
import numpy as np

img = cv.imread('honda.png', cv.IMREAD_GRAYSCALE)

cv.imshow("gambar", img)
cv.waitKey(0)
cv.destroyAllWindows()
