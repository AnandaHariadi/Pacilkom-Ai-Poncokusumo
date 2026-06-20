import numpy as np

def classify_kualitas_apel(image):
    """Klasifikasi CNN (Mock) untuk citra apel berdasarkan warna dan warna dasar citra."""
    classes = ['Sehat', 'Cacat', 'Busuk']
    
    if image.mode != 'RGB':
        image = image.convert('RGB')
    np_img = np.array(image)
    
    mean_r = np.mean(np_img[:, :, 0])
    mean_g = np.mean(np_img[:, :, 1])
    mean_b = np.mean(np_img[:, :, 2])
    
    # Simple heuristic
    if mean_r > 150 and mean_g < 100:
        max_idx = 0 # Sehat (Red)
    elif mean_g > 120 and mean_r > 120 and mean_b < 100:
        max_idx = 0 # Sehat (Green)
    elif mean_r < 100 and mean_g < 100 and mean_b < 100:
        max_idx = 2 # Busuk (Dark)
    else:
        # Check if there are large variations/spots
        std_r = np.std(np_img[:, :, 0])
        if std_r > 60:
            max_idx = 1 # Cacat (Spots/varying)
        else:
            max_idx = 0 # Fallback
            
    probabilities = [0.005, 0.005, 0.005]
    probabilities[max_idx] = 0.99
    
    # Add slight random noise to confidence
    probabilities[max_idx] -= np.random.uniform(0.001, 0.005)
    rem = 1.0 - probabilities[max_idx]
    p1 = rem / 2
    p2 = rem / 2
    idx = 0
    for i in range(3):
        if i != max_idx:
            probabilities[i] = p1 if idx == 0 else p2
            idx += 1
            
    confidence = {c: round(p*100, 2) for c, p in zip(classes, probabilities)}
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
