def get_lime_explanation(text):
    """Mendapatkan highlight LIME (mock)."""
    # Simply highlight key sentiment words
    words = text.split()
    highlighted = []
    for w in words:
        if w.lower() in ['bagus', 'manis', 'segar']:
            highlighted.append(f"<span style='background-color:#c8e6c9'>{w}</span>")
        elif w.lower() in ['busuk', 'jelek', 'kecewa']:
            highlighted.append(f"<span style='background-color:#ffcdd2'>{w}</span>")
        else:
            highlighted.append(w)
            
    return " ".join(highlighted)
