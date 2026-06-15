import matplotlib.pyplot as plt
import numpy as np

def generate_shap_summary_plot():
    """Mengembalikan dummy plot SHAP."""
    features = ['Suhu', 'Curah Hujan', 'Kelembapan', 'Pupuk']
    importance = [0.4, 0.35, 0.1, 0.15]
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(features, importance, color='forestgreen')
    ax.set_xlabel('Mean |SHAP value| (Impact on Model Output)')
    ax.set_title('SHAP Summary Plot (Feature Importance)')
    plt.tight_layout()
    return fig
