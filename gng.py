"""
1-Intro.py
Materi:
1. Read Image
2. Show Image
3. Filter Color (Image)
4. Filter Color (Video)

Catatan: sesuaikan nama file gambar ("honda.png") dan device kamera
kalau diperlukan. Path gambar dibuat relatif terhadap folder script ini
supaya bisa dijalankan dari direktori mana pun.
"""

import cv2
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "honda.png")


# =========================================================
# 1. READ IMAGE
# =========================================================
def read_image(path):
    img = cv2.imread(path)

    if img is None:
        raise FileNotFoundError(f"Gambar tidak ditemukan di: {path}")

    print(f"Gambar berhasil dibaca. Ukuran: {img.shape}")
    return img


# =========================================================
# 2. SHOW IMAGE
# =========================================================
def show_image(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# =========================================================
# 3. FILTER COLOR (IMAGE)
# =========================================================
def filter_color_image(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Contoh: filter warna merah (ubah sesuai kebutuhan)
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    result = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow("Original", img)
    cv2.imshow("Mask", mask)
    cv2.imshow("Filtered Color (Image)", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# =========================================================
# 4. FILTER COLOR (VIDEO)
# =========================================================
def filter_color_video(camera_index=0):
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        raise RuntimeError("Kamera tidak bisa dibuka. Cek device index-nya.")

    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    print("Tekan 'q' untuk keluar dari mode video filter.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal membaca frame dari kamera.")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_red, upper_red)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow("Original (Video)", frame)
        cv2.imshow("Mask (Video)", mask)
        cv2.imshow("Filtered Color (Video)", result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    img = read_image(IMAGE_PATH)

    show_image("Image Original", img)

    filter_color_image(img)

    filter_color_video(0)