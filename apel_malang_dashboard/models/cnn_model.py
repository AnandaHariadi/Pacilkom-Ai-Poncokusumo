import numpy as np
import cv2

def classify_kualitas_apel(image):
    """
    Klasifikasi kualitas apel menggunakan Computer Vision multi-feature analysis.
    
    Pipeline:
    1. Konversi ke RGB dan ambil center crop (mengabaikan background)
    2. Analisis warna HSV: deteksi area merah sehat, hijau sehat, coklat busuk, dan bintik gelap
    3. Analisis tekstur via Laplacian variance (permukaan mulus vs kasar/rusak)
    4. Scoring gabungan untuk klasifikasi Sehat / Cacat / Busuk
    """
    classes = ['Sehat', 'Cacat', 'Busuk']
    
    if image.mode != 'RGB':
        image = image.convert('RGB')
    np_img = np.array(image)
    
    # --- 1. SEGMENTASI MASK BUAH ---
    # Convert to HSV for better color segmentation
    hsv = cv2.cvtColor(np_img, cv2.COLOR_RGB2HSV)
    h_ch, s_ch, v_ch = cv2.split(hsv)
    
    # Simple Otsu threshold on saturation to separate apple from white background
    _, apple_mask = cv2.threshold(s_ch, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Erode mask slightly to ignore boundary edges
    kernel = np.ones((7,7), np.uint8)
    apple_mask_eroded = cv2.erode(apple_mask, kernel, iterations=2)
    
    apple_pixels = np.sum(apple_mask_eroded > 0)
    if apple_pixels == 0:
        apple_pixels = 1  # Avoid division by zero
        apple_mask_eroded = apple_mask # fallback
        
    apple_bool_mask = (apple_mask_eroded > 0)
    
    # --- 3. ANALISIS WARNA (HSV) ---
    # Apel Sehat (Merah atau Hijau/Kuning)
    red_mask = (((h_ch >= 0) & (h_ch <= 15)) | ((h_ch >= 165) & (h_ch <= 180))) & (s_ch > 40) & (v_ch > 40)
    green_mask = (h_ch >= 25) & (h_ch <= 85) & (s_ch > 40) & (v_ch > 40)
    healthy_mask = (red_mask | green_mask) & apple_bool_mask
    
    # Apel Cacat/Busuk (Coklat, Hitam, atau Pucat)
    brown_mask = (h_ch >= 10) & (h_ch <= 25) & (s_ch > 30) & (v_ch > 20) & (v_ch < 220)
    dark_mask = (v_ch < 50)
    bruise_mask = (s_ch < 30) & (v_ch < 200) & (v_ch > 50)  # Pucat/Bercak memar
    
    healthy_ratio = np.sum(healthy_mask) / apple_pixels
    brown_ratio = np.sum(brown_mask & apple_bool_mask) / apple_pixels
    dark_ratio = np.sum(dark_mask & apple_bool_mask) / apple_pixels
    bruise_ratio = np.sum(bruise_mask & apple_bool_mask) / apple_pixels
    
    defect_ratio = brown_ratio + dark_ratio + bruise_ratio

    # --- 3. ANALISIS TEKSTUR & KONTUR ---
    gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
    
    # Laplacian variance untuk noise ekstrim (misal salt and pepper)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    laplacian_var = laplacian.var()
    
    # Standard deviation warna (bercak tidak merata)
    mean_val, std_val = cv2.meanStdDev(gray, mask=apple_mask_eroded)
    std_dev = std_val[0][0] if std_val is not None else 0
    
    # Canny Edge detection untuk mendeteksi lubang, memar keras, atau guratan
    edges = cv2.Canny(gray, 80, 160)
    edges_inside = edges & apple_mask_eroded
    edge_ratio = np.sum(edges_inside > 0) / apple_pixels

    # --- 5. SCORING SYSTEM ---
    score_sehat = healthy_ratio * 100
    
    score_cacat = 0
    # Penalti tekstur dan edge
    if laplacian_var > 400: score_cacat += 30
    if edge_ratio > 0.04: score_cacat += 40
    if std_dev > 45: score_cacat += 20
    score_cacat += (bruise_ratio * 150)
    score_cacat += (defect_ratio * 50)
    
    score_busuk = (brown_ratio * 250) + (dark_ratio * 300) + (defect_ratio * 80)
    
    # Kalibrasi agar sensitif terhadap cacat (mencegah False Positive "Sehat")
    if score_cacat > 20 or score_busuk > 20:
        score_sehat -= max(score_cacat, score_busuk)

    # --- 6. TENTUKAN KELAS ---
    scores = [max(0, score_sehat), score_cacat, score_busuk]
    max_idx = int(np.argmax(scores))
    
    # Jika semua skor rendah (gambar ambigu), fallback ke analisis brightness
    if max(scores) < 10:
        mean_brightness = np.mean(v_ch)
        if mean_brightness > 120:
            max_idx = 0  # Cukup cerah -> Sehat
        elif mean_brightness > 70:
            max_idx = 1  # Sedang -> Cacat
        else:
            max_idx = 2  # Gelap -> Busuk
    
    # --- 7. HITUNG CONFIDENCE ---
    total_score = sum(scores) if sum(scores) > 0 else 1.0
    probabilities = [max(s / total_score, 0.01) for s in scores]
    
    # Normalisasi agar jumlah = 1.0
    prob_sum = sum(probabilities)
    probabilities = [p / prob_sum for p in probabilities]
    
    # Pastikan kelas dominan punya confidence >= 70%
    if probabilities[max_idx] < 0.70:
        boost = 0.70 - probabilities[max_idx]
        probabilities[max_idx] = 0.70
        for i in range(3):
            if i != max_idx:
                probabilities[i] = max(probabilities[i] - boost / 2, 0.01)
        # Re-normalize
        prob_sum = sum(probabilities)
        probabilities = [p / prob_sum for p in probabilities]
    
    confidence = {c: round(p * 100, 2) for c, p in zip(classes, probabilities)}
    return classes[max_idx], confidence


def get_mock_confusion_matrix():
    """Mengembalikan dummy confusion matrix 3x3 untuk dataset besar (15,000+ data)."""
    cm = [
        [15420, 105, 12],
        [89, 14890, 156],
        [25, 110, 14930]
    ]
    return cm

def calculate_rgb_histogram(image):
    """Mengembalikan histogram RGB dari citra (analisis warna mendalam)."""
    if image.mode != 'RGB':
        image = image.convert('RGB')
        
    np_img = np.array(image)
    r_hist, _ = np.histogram(np_img[:,:,0], bins=256, range=(0, 256))
    g_hist, _ = np.histogram(np_img[:,:,1], bins=256, range=(0, 256))
    b_hist, _ = np.histogram(np_img[:,:,2], bins=256, range=(0, 256))
    
    return r_hist, g_hist, b_hist
