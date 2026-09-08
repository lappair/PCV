import cv2
import numpy as np

img = cv2.imread("honda.png")
cv2.imshow("Image Original", img)


#these are channels ) 0 = blue 1 = green = red
#[tinggi, lebar, channel]

red_img = img.copy()
red_img[:,:,0] = 0
red_img[:,:,1] = 0 


green_img = img.copy()
green_img[:,:,0] = 0
green_img[:,:,2] = 0 

blue_img = img.copy()
blue_img[:,:,2] = 0
blue_img[:,:,1] = 0 
cv2.imshow("red", red_img)
cv2.imshow("green", green_img)
cv2.imshow("blue", blue_img)
cv2.waitKey(0)
cv2.destroyAllWindows()