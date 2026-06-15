import numpy as np

def classify_kualitas_apel(image):
    """Klasifikasi CNN (Mock) untuk citra apel."""
    classes = ['Sehat', 'Cacat', 'Busuk']
    # Simulate high confidence predictions
    base_probs = np.random.dirichlet(np.ones(3), size=1)[0]
    max_idx = np.argmax(base_probs)
    probabilities = [0.01, 0.01, 0.01]
    probabilities[max_idx] = 0.98
    
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
