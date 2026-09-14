import cv2
import numpy as np

#imread dan imshow
img = cv2.imread("honda.png")
cv2.imshow("Image Original", img)


#colorfilter(red only, blue only, green only)
red_img = img.copy()
red_img[:,:,0] = 0
red_img[:,:,1] = 0 

green_img = img.copy()
green_img[:,:,0] = 0
green_img[:,:,2] = 0 

blue_img = img.copy()
blue_img[:,:,2] = 0
blue_img[:,:,1] = 0 

hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
sat_scale = 8
hsv_img[:, :, 1] = hsv_img[:, :, 1] * sat_scale

hsv_img = hsv_img.astype(np.uint8)
saturated_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)
cv2.imshow("Increased Saturation", saturated_img)

cv2.imshow("red", red_img)
cv2.imshow("green", green_img)
cv2.imshow("blue", blue_img)
cv2.waitKey(0)
cv2.destroyAllWindows()


#filtervideo
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        break

    red_frame = frame.copy()
    red_frame[:,:,0] = 0
    red_frame[:,:,1] = 0

    green_frame = frame.copy()
    green_frame[:,:,0] = 0
    green_frame[:,:,2] = 0

    blue_frame = frame.copy()
    blue_frame[:,:,2] = 0
    blue_frame[:,:,1] = 0

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv_frame[:, :, 1] = np.clip(hsv_frame[:, :, 1] * sat_scale, 0, 255)
    hsv_frame = hsv_frame.astype(np.uint8)
    saturated_frame = cv2.cvtColor(hsv_frame, cv2.COLOR_HSV2BGR)

    cv2.imshow("Video Original", frame)
    cv2.imshow("Video Red", red_frame)
    cv2.imshow("Video Green", green_frame)
    cv2.imshow("Video Blue", blue_frame)
    cv2.imshow("Video Saturated", saturated_frame)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()