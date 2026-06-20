import os
from PIL import Image
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'apel_malang_dashboard'))
from models.cnn_model import classify_kualitas_apel

images_to_test = [
    r"C:\Users\ASUS TUF\Downloads\apple sehat\rotated_by_30_Screen Shot 2018-06-08 at 5.19.28 PM.png",
    r"C:\Users\ASUS TUF\Downloads\apple sehat\rotated_by_30_Screen Shot 2018-06-08 at 5.20.17 PM.png",
    r"C:\Users\ASUS TUF\Downloads\apple sehat\translation_Screen Shot 2018-06-08 at 5.21.56 PM.png",
    r"C:\Users\ASUS TUF\Downloads\apple sehat\vertical_flip_Screen Shot 2018-06-08 at 5.00.43 PM.png",
    r"C:\Users\ASUS TUF\Downloads\apple sehat\rotated_by_75_Screen Shot 2018-06-08 at 5.20.08 PM.png",
    r"C:\Users\ASUS TUF\Downloads\apple sehat\saltandpepper_Screen Shot 2018-06-08 at 5.16.28 PM.png",
    r"C:\Users\ASUS TUF\Downloads\apple sehat\rotated_by_45_Screen Shot 2018-06-08 at 5.11.41 PM.png",
    r"C:\Users\ASUS TUF\Downloads\apple sehat\rotated_by_60_Screen Shot 2018-06-08 at 5.27.06 PM.png",
    r"C:\Users\ASUS TUF\Downloads\apple sehat\rotated_by_15_Screen Shot 2018-06-08 at 5.27.19 PM.png"
]

correct = 0
total = 0

print("Mulai pengujian CNN untuk citra apel sehat...\n")
for img_path in images_to_test:
    if os.path.exists(img_path):
        try:
            img = Image.open(img_path)
            label, conf = classify_kualitas_apel(img)
            status = "BENAR" if label == "Sehat" else "SALAH"
            if label == "Sehat": correct += 1
            total += 1
            print(f"[{status}] {os.path.basename(img_path)} -> Diprediksi: {label} (Conf: {conf})")
        except Exception as e:
            print(f"[ERROR] Gagal memproses {os.path.basename(img_path)}: {e}")
    else:
        print(f"[SKIP] File tidak ditemukan: {os.path.basename(img_path)}")

if total > 0:
    print(f"\nAkurasi: {correct}/{total} ({(correct/total)*100:.2f}%)")
else:
    print("\nTidak ada gambar yang berhasil diuji.")
