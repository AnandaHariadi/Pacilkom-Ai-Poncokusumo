def integrate_factors_gnn(prediksi_panen, kualitas, sentimen):
    """Pemodelan GNN (Mock) untuk Rekomendasi Harga."""
    base_harga = 18000 
    
    if prediksi_panen > 60:
        base_harga -= 2500 
    elif prediksi_panen < 40:
        base_harga += 3500 
        
    if kualitas == 'Sehat':
        base_harga += 4500
    elif kualitas == 'Busuk':
        base_harga -= 6000
        
    if sentimen == 'Positif':
        base_harga += 1500
    elif sentimen == 'Negatif':
        base_harga -= 2000
        
    return max(6000, base_harga)

def get_mock_price_trend():
    waktu = [f'Minggu {i}' for i in range(1, 21)]
    harga = [15000 + (i*150) + (-1)**i * 500 for i in range(20)]
    return waktu, harga
    
def get_graph_centrality():
    """Kalkulasi Degree Centrality Mock untuk node GNN."""
    return {
        'Hasil Panen': 0.65,
        'Harga': 0.88,
        'Kualitas Fisik': 0.72,
        'Cuaca': 0.45,
        'Persepsi Konsumen': 0.55
    }
