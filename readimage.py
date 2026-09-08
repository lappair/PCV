import cv2 as cv
import numpy as np

img = cv.imread('honda.png', cv.IMREAD_GRAYSCALE)

if img is None:
    raise FileNotFoundError("errorgng")
cv.imshow("gambar", img)
cv.waitKey(0)
cv.destroyAllWindows()
