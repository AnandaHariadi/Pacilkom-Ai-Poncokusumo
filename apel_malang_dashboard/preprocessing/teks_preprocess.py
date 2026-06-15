import re

def clean_and_tokenize(text):
    """Membersihkan teks dan tokenisasi sederhana."""
    text = re.sub(r'[^\w\s]', '', text)
    tokens = text.lower().split()
    return tokens
