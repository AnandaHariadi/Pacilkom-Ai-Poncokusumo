import os
from PIL import Image
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'apel_malang_dashboard'))
from models.cnn_model import classify_kualitas_apel

images_to_test = [
    r"C:\Users\ASUS TUF\Downloads\Apple Busuk cacat\vertical_flip_Screen Shot 2018-06-07 at 2.38.28 PM.png",
    r"C:\Users\ASUS TUF\Downloads\Apple Busuk cacat\vertical_flip_Screen Shot 2018-06-07 at 2.45.18 PM.png",
    r"C:\Users\ASUS TUF\Downloads\Apple Busuk cacat\saltandpepper_Screen Shot 2018-06-08 at 2.34.47 PM.png",
    r"C:\Users\ASUS TUF\Downloads\Apple Busuk cacat\translation_Screen Shot 2018-06-07 at 2.35.21 PM.png",
    r"C:\Users\ASUS TUF\Downloads\Apple Busuk cacat\rotated_by_75_Screen Shot 2018-06-07 at 2.38.38 PM.png",
    r"C:\Users\ASUS TUF\Downloads\Apple Busuk cacat\rotated_by_75_Screen Shot 2018-06-08 at 2.40.38 PM.png",
    r"C:\Users\ASUS TUF\Downloads\Apple Busuk cacat\saltandpepper_Screen Shot 2018-06-07 at 2.15.34 PM.png",
    r"C:\Users\ASUS TUF\Downloads\Apple Busuk cacat\rotated_by_45_Screen Shot 2018-06-08 at 2.37.19 PM.png",
    r"C:\Users\ASUS TUF\Downloads\Apple Busuk cacat\rotated_by_60_Screen Shot 2018-06-07 at 2.22.00 PM.png",
    r"C:\Users\ASUS TUF\Downloads\Apple Busuk cacat\rotated_by_30_Screen Shot 2018-06-07 at 3.06.06 PM.png",
    r"C:\Users\ASUS TUF\Downloads\Apple Busuk cacat\rotated_by_15_Screen Shot 2018-06-08 at 2.40.30 PM.png",
    r"C:\Users\ASUS TUF\Downloads\Apple Busuk cacat\vertical_flip_Screen Shot 2018-06-08 at 2.24.46 PM.png"
]

correct = 0
total = 0

print("Mulai pengujian CNN untuk citra apel busuk/cacat...\n")
for img_path in images_to_test:
    if os.path.exists(img_path):
        try:
            img = Image.open(img_path)
            label, conf = classify_kualitas_apel(img)
            # Karena dataset ini campuran Busuk dan Cacat,
            # asalkan tidak diprediksi "Sehat", maka kita anggap BENAR untuk deteksi bad apple.
            status = "BENAR" if label in ["Cacat", "Busuk"] else "SALAH"
            if label in ["Cacat", "Busuk"]: correct += 1
            total += 1
            print(f"[{status}] {os.path.basename(img_path)} -> Diprediksi: {label} (Conf: {conf})")
        except Exception as e:
            print(f"[ERROR] Gagal memproses {os.path.basename(img_path)}: {e}")
    else:
        print(f"[SKIP] File tidak ditemukan: {os.path.basename(img_path)}")

if total > 0:
    print(f"\nAkurasi Tangkapan Apel Buruk: {correct}/{total} ({(correct/total)*100:.2f}%)")
else:
    print("\nTidak ada gambar yang berhasil diuji.")
