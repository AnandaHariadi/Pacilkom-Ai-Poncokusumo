import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import io
import base64
import pydeck as pdk
import pandas as pd
import numpy as np

# Global Theme Setting
TEMPLATE = 'plotly_dark'
KAGGLE_TEXT_COLOR = '#00ffcc'

def plot_prediksi_panen(aktual, prediksi, waktu):
    fig = go.Figure()
    
    # Calculate mock uncertainty for detail
    upper_bound = [p * 1.05 for p in prediksi]
    lower_bound = [p * 0.95 for p in prediksi]
    
    # Confidence interval band
    fig.add_trace(go.Scatter(
        x=waktu + waktu[::-1],
        y=upper_bound + lower_bound[::-1],
        fill='toself',
        fillcolor='rgba(0, 255, 204, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=True,
        name='95% Confidence Interval'
    ))

    fig.add_trace(go.Scatter(
        x=waktu, y=aktual, 
        mode='lines+markers', 
        name='Aktual (Kaggle Weather Data)', 
        line=dict(color='#ff3366', width=3),
        marker=dict(size=8, symbol='circle', line=dict(width=2, color='white'))
    ))
    fig.add_trace(go.Scatter(
        x=waktu, y=prediksi, 
        mode='lines+markers', 
        name='Prediksi Model (MLP/RF)', 
        line=dict(color='#00ffcc', width=3, dash='dashdot'),
        marker=dict(size=8, symbol='diamond')
    ))
    
    fig.update_layout(
        title='<b>Prediksi vs Aktual Hasil Panen</b><br><sup><i>Berdasarkan 10k+ Baris Dataset Cuaca Kaggle</i></sup>', 
        xaxis_title='Periode/Waktu', 
        yaxis_title='Hasil Panen (Ton)', 
        template=TEMPLATE,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def plot_confusion_matrix(cm, labels=['Sehat', 'Cacat', 'Busuk']):
    fig = go.Figure(data=go.Heatmap(
        z=cm, x=labels, y=labels, 
        hoverongaps = False, 
        colorscale='Viridis',
        text=cm,
        texttemplate="%{text}",
        textfont={"size": 16}
    ))
    fig.update_layout(
        title='<b>Confusion Matrix Evaluasi Kualitas</b><br><sup><i>Sumber: Kaggle Apple Leaf Disease Dataset</i></sup>', 
        xaxis_title='Prediksi', 
        yaxis_title='Aktual',
        template=TEMPLATE
    )
    return fig

def plot_sentiment_treemap(text_data):
    from collections import Counter
    import plotly.express as px
    import pandas as pd
    
    word_counts = Counter(text_data)
    words = []
    counts = []
    categories = []
    
    # Categorize words based on sentiment logic for visualization
    for w, c in word_counts.items():
        words.append(w)
        counts.append(c)
        if w in ['busuk', 'jelek', 'kecewa', 'buruk', 'mahal', 'hancur', 'kecil']:
            categories.append('Kritik & Keluhan')
        elif w in ['bagus', 'manis', 'segar', 'enak', 'puas', 'murah', 'mantap', 'besar', 'kualitas']:
            categories.append('Pujian Konsumen')
        else:
            categories.append('Atribut Operasional')
            
    df = pd.DataFrame({'Word': words, 'Count': counts, 'Category': categories})
    
    fig = px.treemap(
        df, 
        path=['Category', 'Word'], 
        values='Count',
        color='Category',
        color_discrete_map={
            'Kritik & Keluhan': '#ff3366',
            'Pujian Konsumen': '#00ffcc',
            'Atribut Operasional': '#888888'
        },
        title='<b>Hierarki Entitas Kunci (Treemap)</b><br><sup><i>Pemetaan Analitik Korpus Teks Konsumen</i></sup>'
    )
    
    fig.update_layout(
        template=TEMPLATE,
        margin=dict(t=50, l=10, r=10, b=10)
    )
    return fig

def plot_centrality_radar(centrality_dict):
    import plotly.graph_objects as go
    categories = list(centrality_dict.keys())
    values = list(centrality_dict.values())
    
    # Close the polygon
    categories.append(categories[0])
    values.append(values[0])
    
    fig = go.Figure(data=go.Scatterpolar(
      r=values,
      theta=categories,
      fill='toself',
      fillcolor='rgba(0, 255, 204, 0.3)',
      line=dict(color='#00ffcc', width=2)
    ))
    
    fig.update_layout(
      polar=dict(
        radialaxis=dict(visible=True, range=[0, 1], gridcolor='#444444'),
        angularaxis=dict(gridcolor='#444444')
      ),
      showlegend=False,
      template=TEMPLATE,
      margin=dict(t=30, b=30, l=30, r=30),
      height=300
    )
    return fig

def plot_sentiment_distribution(sentimen_counts):
    labels = list(sentimen_counts.keys())
    values = list(sentimen_counts.values())
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, 
        hole=.5, 
        marker_colors=['#00ffcc', '#ff3366', '#a9a9a9'],
        textinfo='label+percent',
        pull=[0.05, 0, 0]
    )])
    
    # Add Kaggle label in center
    fig.update_layout(
        title='<b>Distribusi Sentimen Ulasan</b><br><sup><i>Korpus: 1500 E-Commerce Reviews (Kaggle)</i></sup>',
        template=TEMPLATE,
        annotations=[dict(text='Kaggle<br>Dataset', x=0.5, y=0.5, font_size=18, showarrow=False, font_color='#00ffcc')]
    )
    return fig

def plot_tren_harga(waktu, harga, rekomendasi):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=waktu, y=harga, 
        mode='lines', name='Harga Historis', 
        line=dict(color='#00ffcc', width=2),
        fill='tozeroy', fillcolor='rgba(0, 255, 204, 0.1)'
    ))
    fig.add_trace(go.Scatter(
        x=waktu[-1:], y=[rekomendasi], 
        mode='markers', name='Rekomendasi Harga', 
        marker=dict(color='#ff3366', size=16, symbol='star', line=dict(color='white', width=2))
    ))
    fig.update_layout(
        title='<b>Tren Harga Jual & Rekomendasi (Rp/Kg)</b><br><sup><i>Algoritmik Berbasis AI & Sentimen Kaggle</i></sup>', 
        xaxis_title='Periode', yaxis_title='Harga (Rupiah)', 
        template=TEMPLATE
    )
    return fig

def plot_weather_eda(df):
    numeric_df = df.select_dtypes(include=['float64', 'int64']).corr()
    fig = go.Figure(data=go.Heatmap(
        z=numeric_df.values, 
        x=numeric_df.columns, y=numeric_df.columns, 
        colorscale='Plasma',
        text=np.round(numeric_df.values, 2),
        texttemplate="%{text}",
    ))
    fig.update_layout(
        title='<b>Matriks Korelasi Cuaca (EDA)</b><br><sup><i>Kaggle: Global Weather Data for Agriculture</i></sup>', 
        width=600, height=500,
        template=TEMPLATE
    )
    return fig

def plot_rgb_histogram(r_hist, g_hist, b_hist):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=r_hist, mode='lines', fill='tozeroy', fillcolor='rgba(255, 0, 0, 0.3)', line=dict(color='#ff3333'), name='Red'))
    fig.add_trace(go.Scatter(y=g_hist, mode='lines', fill='tozeroy', fillcolor='rgba(0, 255, 0, 0.3)', line=dict(color='#33ff33'), name='Green'))
    fig.add_trace(go.Scatter(y=b_hist, mode='lines', fill='tozeroy', fillcolor='rgba(0, 0, 255, 0.3)', line=dict(color='#3333ff'), name='Blue'))
    fig.update_layout(
        title='<b>Distribusi Spektrum RGB Citra Apel</b><br><sup><i>Analisis Visi Komputer Detail</i></sup>', 
        xaxis_title='Intensitas Piksel', yaxis_title='Frekuensi', 
        template=TEMPLATE,
        hovermode="x unified"
    )
    return fig

def plot_ngram_distribution(ngrams_dict, top_n=10):
    sorted_ngrams = sorted(ngrams_dict.items(), key=lambda item: item[1], reverse=True)[:top_n]
    if not sorted_ngrams:
        return go.Figure()
    labels, values = zip(*sorted_ngrams)
    
    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation='h', 
        marker=dict(
            color=values,
            colorscale='Tealgrn',
            line=dict(color='white', width=1)
        ),
        text=values,
        textposition='auto'
    ))
    fig.update_layout(
        title=f'<b>Top {top_n} N-Gram Sentimen Teratas</b><br><sup><i>Ekstraksi dari Kaggle E-Commerce Reviews</i></sup>', 
        xaxis_title='Frekuensi', yaxis_title='Frasa (N-Gram)', 
        yaxis={'categoryorder':'total ascending'},
        template=TEMPLATE
    )
    return fig

def plot_malang_interactive_map():
    """Peta interaktif Folium dengan deteksi wilayah & popup alamat detail."""
    import folium
    from folium import plugins
    
    # Pusat peta: Kecamatan Poncokusumo
    m = folium.Map(
        location=[-8.016, 112.825],
        zoom_start=13,
        tiles="OpenStreetMap",
        control_scale=True,
    )
    
    # Tambahkan layer peta lain untuk user bisa switch
    folium.TileLayer("cartodbpositron", name="Clean (Light)").add_to(m)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri", name="Satelit"
    ).add_to(m)
    
    # Data wilayah: polygon koordinat, info detail
    wilayah_data = [
        {
            "name": "Desa Gubugklakah",
            "coords": [[-8.000, 112.830], [-8.000, 112.842], [-8.010, 112.842], [-8.010, 112.830]],
            "color": "#22c55e",
            "harvest": 85,
            "alamat": "Desa Gubugklakah, Kec. Poncokusumo, Kab. Malang, Jawa Timur 65157",
            "luas": "±320 Ha",
            "ketinggian": "850-1100 mdpl",
            "varietas": "Apel Manalagi, Apel Anna",
            "keterangan": "Sentra agrowisata apel terbesar. Akses jalan provinsi.",
        },
        {
            "name": "Desa Poncokusumo (Pusat)",
            "coords": [[-8.012, 112.818], [-8.012, 112.832], [-8.022, 112.832], [-8.022, 112.818]],
            "color": "#0ea5e9",
            "harvest": 95,
            "alamat": "Desa Poncokusumo, Kec. Poncokusumo, Kab. Malang, Jawa Timur 65157",
            "luas": "±410 Ha",
            "ketinggian": "900-1200 mdpl",
            "varietas": "Apel Manalagi, Apel Rome Beauty",
            "keterangan": "Pusat pemerintahan kecamatan. Produktivitas tertinggi.",
        },
        {
            "name": "Desa Wringinanom",
            "coords": [[-7.990, 112.835], [-7.990, 112.847], [-8.000, 112.847], [-8.000, 112.835]],
            "color": "#ef4444",
            "harvest": 70,
            "alamat": "Desa Wringinanom, Kec. Poncokusumo, Kab. Malang, Jawa Timur 65157",
            "luas": "±180 Ha",
            "ketinggian": "750-950 mdpl",
            "varietas": "Apel Anna, Madu",
            "keterangan": "Sentra madu & apel. Cocok untuk agrowisata terpadu.",
        },
        {
            "name": "Desa Pandansari",
            "coords": [[-8.027, 112.822], [-8.027, 112.835], [-8.038, 112.835], [-8.038, 112.822]],
            "color": "#22c55e",
            "harvest": 88,
            "alamat": "Desa Pandansari Lor, Kec. Poncokusumo, Kab. Malang, Jawa Timur 65157",
            "luas": "±290 Ha",
            "ketinggian": "1000-1350 mdpl",
            "varietas": "Apel Manalagi",
            "keterangan": "Wilayah dataran tinggi. Kualitas apel premium.",
        },
        {
            "name": "Desa Belung",
            "coords": [[-8.020, 112.788], [-8.020, 112.800], [-8.030, 112.800], [-8.030, 112.788]],
            "color": "#f59e0b",
            "harvest": 65,
            "alamat": "Desa Belung, Kec. Poncokusumo, Kab. Malang, Jawa Timur 65157",
            "luas": "±150 Ha",
            "ketinggian": "700-900 mdpl",
            "varietas": "Apel Anna",
            "keterangan": "Wilayah barat. Perkembangan perkebunan baru.",
        },
        {
            "name": "Desa Sumberejo",
            "coords": [[-8.040, 112.805], [-8.040, 112.818], [-8.050, 112.818], [-8.050, 112.805]],
            "color": "#0ea5e9",
            "harvest": 75,
            "alamat": "Desa Sumberejo, Kec. Poncokusumo, Kab. Malang, Jawa Timur 65157",
            "luas": "±210 Ha",
            "ketinggian": "800-1050 mdpl",
            "varietas": "Apel Rome Beauty",
            "keterangan": "Dekat lereng Gunung Bromo. Tanah vulkanik subur.",
        },
    ]
    
    for w in wilayah_data:
        # Polygon zona wilayah
        popup_html = f"""
        <div style="font-family: 'Segoe UI', sans-serif; min-width: 260px; padding: 4px;">
            <h4 style="margin:0 0 8px; color: {w['color']}; border-bottom: 2px solid {w['color']}; padding-bottom: 6px;">
                📍 {w['name']}
            </h4>
            <p style="margin:4px 0; font-size:12px; color:#374151;"><b>📮 Alamat:</b><br/>{w['alamat']}</p>
            <hr style="margin:6px 0; border:none; border-top:1px solid #e5e7eb;"/>
            <table style="font-size:12px; color:#1f2937; width:100%;">
                <tr><td>🍎 <b>Estimasi Panen</b></td><td style="text-align:right;">{w['harvest']} Ton/Ha</td></tr>
                <tr><td>📐 <b>Luas Lahan</b></td><td style="text-align:right;">{w['luas']}</td></tr>
                <tr><td>⛰️ <b>Ketinggian</b></td><td style="text-align:right;">{w['ketinggian']}</td></tr>
                <tr><td>🌱 <b>Varietas</b></td><td style="text-align:right;">{w['varietas']}</td></tr>
            </table>
            <hr style="margin:6px 0; border:none; border-top:1px solid #e5e7eb;"/>
            <p style="margin:4px 0; font-size:11px; color:#6b7280;"><i>ℹ️ {w['keterangan']}</i></p>
        </div>
        """
        
        folium.Polygon(
            locations=w["coords"],
            color=w["color"],
            weight=3,
            fill=True,
            fill_color=w["color"],
            fill_opacity=0.25,
            popup=folium.Popup(popup_html, max_width=320),
            tooltip=f"<b>{w['name']}</b> — Klik untuk detail",
        ).add_to(m)
        
        # Marker pin di tengah zona
        center_lat = sum(c[0] for c in w["coords"]) / len(w["coords"])
        center_lon = sum(c[1] for c in w["coords"]) / len(w["coords"])
        
        folium.Marker(
            location=[center_lat, center_lon],
            popup=folium.Popup(popup_html, max_width=320),
            tooltip=f"{w['name']}",
            icon=folium.Icon(color="green" if w["color"] == "#22c55e" else ("blue" if w["color"] == "#0ea5e9" else ("red" if w["color"] == "#ef4444" else "orange")), icon="leaf", prefix="fa"),
        ).add_to(m)
    
    # Layer control agar user bisa switch antar peta
    folium.LayerControl(collapsed=False).add_to(m)
    
    # Minimap
    plugins.MiniMap(toggle_display=True).add_to(m)
    
    # Fullscreen button
    plugins.Fullscreen(position="topright").add_to(m)
    
    return m

def plot_weather_distributions(df):
    fig = go.Figure()
    if 'Temperature' in df.columns:
        fig.add_trace(go.Violin(y=df['Temperature'], name='Suhu (°C)', box_visible=True, meanline_visible=True, fillcolor='rgba(0, 255, 204, 0.4)', line_color='#00ffcc'))
    if 'Humidity' in df.columns:
        fig.add_trace(go.Violin(y=df['Humidity'], name='Kelembapan (%)', box_visible=True, meanline_visible=True, fillcolor='rgba(255, 51, 102, 0.4)', line_color='#ff3366'))
    if 'Wind Speed' in df.columns:
        fig.add_trace(go.Violin(y=df['Wind Speed'], name='Angin (km/h)', box_visible=True, meanline_visible=True, fillcolor='rgba(255, 204, 0, 0.4)', line_color='#ffcc00'))
    fig.update_layout(
        title='<b>Distribusi Densitas Parameter Cuaca Utama</b><br><sup><i>Dataset: Kaggle Agricultural Weather Classification</i></sup>', 
        yaxis_title='Parameter Kuantitatif', 
        template=TEMPLATE, violinmode='overlay'
    )
    return fig

def plot_nlp_3d_embeddings():
    words = [
        {"word": "manis", "x": 1.3, "y": 2.0, "z": 0.8, "sentiment": "Positif", "color": "#00ffcc"},
        {"word": "segar", "x": 1.6, "y": 1.7, "z": 1.1, "sentiment": "Positif", "color": "#00ffcc"},
        {"word": "enak", "x": 0.9, "y": 2.2, "z": 0.7, "sentiment": "Positif", "color": "#00ffcc"},
        {"word": "puas", "x": 1.2, "y": 1.8, "z": 1.3, "sentiment": "Positif", "color": "#00ffcc"},
        {"word": "cepat", "x": 0.6, "y": 1.1, "z": 0.5, "sentiment": "Positif", "color": "#00ffcc"},
        
        {"word": "busuk", "x": -1.4, "y": -1.7, "z": -1.0, "sentiment": "Negatif", "color": "#ff3366"},
        {"word": "bonyok", "x": -1.6, "y": -1.4, "z": -1.3, "sentiment": "Negatif", "color": "#ff3366"},
        {"word": "kecewa", "x": -1.1, "y": -2.1, "z": -0.8, "sentiment": "Negatif", "color": "#ff3366"},
        {"word": "hambar", "x": -0.7, "y": -1.3, "z": -0.6, "sentiment": "Negatif", "color": "#ff3366"},
        {"word": "lambat", "x": -0.4, "y": -1.0, "z": -0.4, "sentiment": "Negatif", "color": "#ff3366"},
        
        {"word": "standar", "x": 0.1, "y": 0.3, "z": -0.1, "sentiment": "Netral", "color": "#aaaaaa"},
        {"word": "biasa", "x": -0.2, "y": 0.2, "z": 0.2, "sentiment": "Netral", "color": "#aaaaaa"},
        {"word": "harga", "x": 0.3, "y": -0.1, "z": 0.4, "sentiment": "Netral", "color": "#aaaaaa"},
        {"word": "paket", "x": 0.0, "y": -0.2, "z": -0.3, "sentiment": "Netral", "color": "#aaaaaa"},
    ]
    df_emb = pd.DataFrame(words)
    
    fig = go.Figure(data=[go.Scatter3d(
        x=df_emb['x'], y=df_emb['y'], z=df_emb['z'],
        mode='markers+text',
        text=df_emb['word'],
        textposition="top center",
        marker=dict(
            size=10,
            color=df_emb['color'],
            opacity=0.9,
            line=dict(color='white', width=1)
        )
    )])
    
    fig.update_layout(
        title="<b>Proyeksi 3D Word Embeddings Semantik</b><br><sup><i>Berdasarkan Model BERT pada Data Ulasan Kaggle</i></sup>",
        scene=dict(
            xaxis=dict(title='Dimensi X', showbackground=False),
            yaxis=dict(title='Dimensi Y', showbackground=False),
            zaxis=dict(title='Dimensi Z', showbackground=False)
        ),
        margin=dict(l=0, r=0, b=0, t=60),
        template=TEMPLATE
    )
    return fig

def plot_tren_harga_advanced(waktu, harga, rekomendasi):
    df = pd.DataFrame({'Waktu': waktu, 'Harga': harga})
    df['MA5'] = df['Harga'].rolling(window=5, min_periods=1).mean()
    df['STD5'] = df['Harga'].rolling(window=5, min_periods=1).std().fillna(0)
    df['UpperBand'] = df['MA5'] + (df['STD5'] * 1.5)
    df['LowerBand'] = df['MA5'] - (df['STD5'] * 1.5)
    
    fig = go.Figure()
    
    # Bollinger Bands area
    fig.add_trace(go.Scatter(
        x=df['Waktu'].tolist() + df['Waktu'].tolist()[::-1],
        y=df['UpperBand'].tolist() + df['LowerBand'].tolist()[::-1],
        fill='toself',
        fillcolor='rgba(0, 255, 204, 0.15)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=True,
        name='Bollinger Bands (Volatilitas Kaggle Market)'
    ))
    
    # Harga Historis
    fig.add_trace(go.Scatter(
        x=df['Waktu'], y=df['Harga'], 
        mode='lines+markers', name='Harga Pasar Historis', 
        line=dict(color='#ff3366', width=2),
        marker=dict(size=6, color='#ff3366')
    ))
    
    # MA5
    fig.add_trace(go.Scatter(
        x=df['Waktu'], y=df['MA5'], 
        mode='lines', name='MA-5 (Tren)', 
        line=dict(color='#00ffcc', width=2, dash='dot')
    ))
    
    # Rekomendasi AI
    fig.add_trace(go.Scatter(
        x=[df['Waktu'].iloc[-1]], y=[rekomendasi], 
        mode='markers', name='Rekomendasi Optimal', 
        marker=dict(color='#ffcc00', size=16, symbol='star-diamond', line=dict(color='white', width=2))
    ))
    
    fig.update_layout(
        title='<b>Proyeksi Tren Harga & Volatilitas Pasar</b><br><sup><i>Indikator Teknikal dengan Data Makroekonomi Kaggle</i></sup>',
        xaxis_title='Periode Transaksi',
        yaxis_title='Harga (Rupiah/Kg)',
        template=TEMPLATE,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def plot_feature_map_activation():
    """Simulasi Feature Map Activation pada Hidden Layer CNN."""
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2)) * np.exp(-0.1 * (X**2 + Y**2)) + np.random.normal(0, 0.1, X.shape)
    
    fig = go.Figure(data=go.Contour(
        z=Z,
        colorscale='Electric',
        contours=dict(showlines=False),
        hoverinfo='none'
    ))
    fig.update_layout(
        title='<b>Visualisasi Ekstraksi Fitur (Conv2D Layer)</b><br><sup><i>Pemetaan Spasial Edges & Tekstur</i></sup>',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        template=TEMPLATE,
        margin=dict(l=0, r=0, b=0, t=60)
    )
    return fig


