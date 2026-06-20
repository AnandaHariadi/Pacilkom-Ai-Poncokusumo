import pandas as pd
import numpy as np
import random
import os

def generate_reviews():
    """Menghasilkan 5000 baris data ulasan e-commerce gaya Kaggle."""
    os.makedirs('../data/teks', exist_ok=True)
    
    np.random.seed(42)
    random.seed(42)
    
    positive_phrases = ["sangat manis", "kualitas super", "pengiriman cepat", "segar sekali", "murah dan bagus", "renyah", "seller ramah", "packing aman", "buahnya besar", "mantap"]
    negative_phrases = ["apel busuk", "rasa hambar", "pengiriman lambat", "kecewa", "ukuran kecil", "banyak yang bonyok", "kurang segar", "harga mahal", "jelek", "hancur"]
    neutral_phrases = ["lumayan", "sesuai harga", "standar", "biasa saja", "oke", "sampai tujuan", "sesuai deskripsi", "cukup", "not bad", "bisa dimakan"]
    
    data = []
    for i in range(5000):
        sentiment_type = np.random.choice(['Positif', 'Negatif', 'Netral'], p=[0.6, 0.2, 0.2])
        
        if sentiment_type == 'Positif':
            phrase1 = random.choice(positive_phrases)
            phrase2 = random.choice(positive_phrases + neutral_phrases)
            text = f"{phrase1}, {phrase2}. Sangat merekomendasikan."
        elif sentiment_type == 'Negatif':
            phrase1 = random.choice(negative_phrases)
            phrase2 = random.choice(negative_phrases)
            text = f"{phrase1}, benar-benar {phrase2}. Tidak akan beli lagi."
        else:
            phrase1 = random.choice(neutral_phrases)
            text = f"Barang {phrase1}, pengiriman standar."
            
        data.append({
            'Review_ID': f"REV{i+1000}",
            'Text': text,
            'Rating': np.random.choice([4, 5]) if sentiment_type == 'Positif' else (np.random.choice([1, 2]) if sentiment_type == 'Negatif' else 3),
            'Sentiment': sentiment_type
        })
        
    df = pd.DataFrame(data)
    df.to_csv('../data/teks/data_ulasan_konsumen.csv', index=False)
    print("Berhasil membuat dataset teks ulasan (5000 baris).")

if __name__ == "__main__":
    generate_reviews()
