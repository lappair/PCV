# Color Filtering dengan OpenCV — Image & Video

Dokumentasi ini menjelaskan program Python yang melakukan filter warna (red/green/blue only) dan peningkatan saturasi pada gambar diam maupun video real-time dari webcam menggunakan OpenCV.

## Struktur Program

Program ini terbagi menjadi dua bagian besar:
1. **Image Processing** — baca gambar statis, filter warna, dan tingkatkan saturasi.
2. **Video Processing** — proses yang sama diterapkan secara real-time per-frame dari webcam.

---

## 1. Bagian Image

### Read & Show Image

```python
img = cv2.imread("honda.png")
cv2.imshow("Image Original", img)
```

`cv2.imread()` membaca file gambar menjadi array NumPy dalam format **BGR** (Blue-Green-Red), bukan RGB. `cv2.imshow()` menampilkannya dalam sebuah window.

### Color Filter (Red / Green / Blue Only)

```python
red_img = img.copy()
red_img[:,:,0] = 0   # Blue channel = 0
red_img[:,:,1] = 0   # Green channel = 0
```

Karena urutan channel di OpenCV adalah **BGR**, index array-nya:
| Index | Channel |
|---|---|
| `[:,:,0]` | Blue |
| `[:,:,1]` | Green |
| `[:,:,2]` | Red |

Untuk menyisakan hanya satu warna, dua channel lainnya di-nolkan:

| Variabel | Channel yang dinolkan | Channel yang tersisa |
|---|---|---|
| `red_img` | Blue, Green | **Red** |
| `green_img` | Blue, Red | **Green** |
| `blue_img` | Green, Red | **Blue** |

`img.copy()` dipakai supaya tiap filter tidak saling menimpa data dari array `img` yang sama (menghindari efek *mutable reference* di NumPy).

### Bonus: Increased Saturation

```python
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
sat_scale = 8
hsv_img[:, :, 1] = hsv_img[:, :, 1] * sat_scale

hsv_img = hsv_img.astype(np.uint8)
saturated_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)
```

Langkah-langkahnya:
1. Konversi dari BGR ke **HSV**, karena saturasi (S) hanya ada sebagai channel eksplisit di ruang warna HSV, tidak ada di BGR.
2. Ubah tipe data ke `float32` agar bisa dikalikan tanpa overflow saat proses perhitungan.
3. Kalikan channel Saturation (index `1`) dengan `sat_scale` untuk menaikkan intensitas warna.
4. Ubah kembali ke `uint8` (rentang 0–255) dan konversi balik ke BGR agar bisa ditampilkan.

> ⚠️ **Catatan:** Pada bagian gambar, hasil perkalian `hsv_img[:, :, 1] * sat_scale` tidak dibatasi dengan `np.clip()`. Jika hasil kali melebihi 255 sebelum di-cast ke `uint8`, nilainya bisa *wrap-around* (contoh: 200 × 8 = 1600 → `1600 % 256 = 64`) sehingga warna menjadi tidak terduga. Bagian video di bawah sudah menerapkan `np.clip()` untuk mencegah hal ini.

---

## 2. Bagian Video

```python
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        break
    ...
```

- `cv2.VideoCapture(0)` membuka kamera default (index `0`).
- Loop `while True` membaca frame terus-menerus selama kamera aktif; `ret` bernilai `False` jika frame gagal diambil.
- Semua proses filter (red/green/blue only, increase saturation) yang sama seperti pada gambar diterapkan ulang di setiap iterasi (per-frame), sehingga hasilnya tampak sebagai efek real-time.

### Perbedaan dengan Saturation di Bagian Image

```python
hsv_frame[:, :, 1] = np.clip(hsv_frame[:, :, 1] * sat_scale, 0, 255)
```

Di bagian video, `np.clip(..., 0, 255)` digunakan untuk membatasi nilai saturasi maksimum sebelum dikonversi ke `uint8`, mencegah overflow/wrap-around warna yang bisa terjadi di bagian gambar.

### Keluar dari Loop

```python
if cv2.waitKey(1) == ord('q'):
    break
```

`cv2.waitKey(1)` menunggu input keyboard selama 1 milidetik per frame (agar video tetap terasa real-time/smooth). Program berhenti saat tombol **`q`** ditekan.

### Cleanup

```python
cam.release()
cv2.destroyAllWindows()
```

Wajib dipanggil di akhir untuk melepas resource kamera dan menutup semua window OpenCV.

---

## Ringkasan Alur Program

1. Baca gambar `honda.png` → tampilkan.
2. Buat 3 versi filter warna (red-only, green-only, blue-only) dari gambar.
3. Naikkan saturasi gambar lewat konversi ke HSV.
4. Tampilkan semua hasil, tunggu tombol apa saja untuk lanjut ke bagian video.
5. Buka webcam, ulangi proses filter warna & saturasi yang sama untuk tiap frame secara real-time.
6. Tekan `q` untuk keluar dan melepas kamera.

## Potensi Pengembangan

- Tambahkan `if img is None: raise FileNotFoundError(...)` setelah `cv2.imread()` untuk menghindari crash `imshow` saat file gambar tidak ditemukan.
- Terapkan `np.clip()` juga pada bagian saturation di gambar (bukan hanya video) untuk konsistensi.
- Gunakan `cv2.inRange()` pada HSV untuk filter warna berbasis rentang warna asli (bukan sekadar channel BGR), misalnya untuk deteksi objek warna tertentu.