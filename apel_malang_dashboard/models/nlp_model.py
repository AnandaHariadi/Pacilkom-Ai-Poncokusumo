import random
from collections import Counter
import re

def analyze_sentiment(text):
    """Analisis sentimen NLP (Mock BERT)."""
    text_lower = text.lower()
    if any(word in text_lower for word in ['busuk', 'jelek', 'kecewa', 'buruk', 'mahal', 'hancur']):
        sentiment = 'Negatif'
    elif any(word in text_lower for word in ['bagus', 'manis', 'segar', 'enak', 'puas', 'murah', 'mantap']):
        sentiment = 'Positif'
    else:
        sentiment = 'Netral'
    return sentiment

def get_mock_sentiment_distribution():
    return {'Positif': 1250, 'Negatif': 420, 'Netral': 380}

def get_mock_wordcloud_data():
    words = ['manis', 'segar', 'renyah', 'kualitas', 'harga', 'cepat', 'murah', 'busuk', 'kecil', 'besar', 'puas', 'merah', 'hijau', 'pengiriman', 'seller', 'mantap']
    text_data = [random.choice(words) for _ in range(1000)]
    return text_data

def extract_ngrams(text, n=2):
    """Ekstraksi N-Gram dari teks untuk analisis mendalam."""
    text = re.sub(r'[^\w\s]', '', text.lower())
    tokens = text.split()
    if len(tokens) < n:
        return {}
    ngrams = zip(*[tokens[i:] for i in range(n)])
    ngrams_str = [" ".join(ngram) for ngram in ngrams]
    return dict(Counter(ngrams_str))
