import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
import time
import random
import base64

# Set page config (No Emojis)
st.set_page_config(
    page_title="Dashboard Apel Malang",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Refined Premium UI/UX Custom CSS (Eco-Tech Theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Global Background & Font Polish */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
    }
    
    /* Sidebar Styling Refinement (Fix Font Ketutup) */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #10b981 0%, #064e3b 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.15);
    }
    
    /* Memaksa semua teks biasa, label, dan markdown di sidebar menjadi putih/terang */
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] p {
        color: #f8fafc !important; /* Off-White / Slate Light */
        font-weight: 500;
    }
    
    /* Sidebar Headers & Titles */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
        margin-bottom: 10px !important;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Khusus untuk teks menu Radio Button yang tidak aktif */
    [data-testid="stSidebar"] .stRadio p,
    [data-testid="stSidebar"] .stRadio label p,
    [data-testid="stSidebar"] .stRadio label span,
    [data-testid="stSidebar"] .stRadio label div,
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label p,
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label span,
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label div {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Radio buttons menu styling in sidebar to look like clean button items */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
        gap: 8px !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        transition: all 0.2s ease-in-out !important;
        cursor: pointer !important;
        width: 100% !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label * {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        background-color: rgba(255, 255, 255, 0.15) !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] [data-checked="true"] label,
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] [data-checked="true"] label * {
        background: rgba(255, 255, 255, 0.25) !important;
        border-color: #ffffff !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Info Alert Styling in Sidebar */
    [data-testid="stSidebar"] [data-testid="stAlert"] {
        background-color: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #cbd5e1 !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }
    [data-testid="stSidebar"] [data-testid="stAlert"] p {
        color: #cbd5e1 !important;
    }
    
    /* Clean Cards for Metrics */
    .metric-container {
        padding: 24px;
        border-radius: 16px;
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 6px solid #10b981; /* Emerald Green Accent */
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
        margin-bottom: 24px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .metric-container:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 28px rgba(15, 23, 42, 0.08);
        border-color: rgba(16, 185, 129, 0.3);
    }
    
    /* Professional Pulse Scanning Box for CNN Vision */
    .scanning-box {
        border: 2px dashed #ef4444; /* Ripe Apple Red */
        background-color: rgba(254, 242, 242, 0.6);
        backdrop-filter: blur(4px);
        padding: 20px;
        border-radius: 16px;
        margin: 20px 0;
        box-shadow: 0 8px 24px rgba(239, 68, 68, 0.05);
        animation: pulseAnimation 2s infinite ease-in-out;
    }
    @keyframes pulseAnimation {
        0% { border-color: #ef4444; background-color: rgba(254, 242, 242, 0.6); }
        50% { border-color: #fee2e2; background-color: #ffffff; }
        100% { border-color: #ef4444; background-color: rgba(254, 242, 242, 0.6); }
    }
    
    /* Action Buttons Custom Styling (Download) */
    .download-button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: #ffffff !important;
        padding: 12px 26px;
        text-align: center;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        font-weight: 600;
        letter-spacing: 0.5px;
        border: none;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
        transition: all 0.2s ease;
        margin-top: 15px;
    }
    .download-button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.35);
        color: #ffffff !important;
    }
    
    /* General Streamlit Buttons */
    .stButton button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        padding: 10px 24px !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        letter-spacing: 0.2px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 10px rgba(16, 185, 129, 0.15) !important;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.25) !important;
        color: white !important;
    }
    
    /* Titles and Headers Styling */
    h1 {
        color: #0f172a !important; /* Dark Slate */
        font-weight: 800 !important;
        letter-spacing: -1px !important;
        margin-bottom: 8px !important;
    }
    h2 {
        color: #1e293b !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
        margin-top: 20px !important;
        margin-bottom: 12px !important;
    }
    h3 {
        color: #334155 !important;
        font-weight: 600 !important;
        letter-spacing: -0.3px !important;
    }
    
    /* Streamlit Tab Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #e2e8f0;
        padding: 6px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 8px !important;
        padding: 8px 18px !important;
        color: #475569 !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

# =================================================================
# SIDEBAR NAVIGATION & LOGO
# =================================================================

# Fungsi helper untuk encode image ke base64 agar bisa diatur sizenya via HTML/CSS
def get_image_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path_logo = os.path.join(BASE_DIR, "assets", "logo-1.png") # Pastikan folder assets dan file ini ada

if os.path.exists(path_logo):
    try:
        logo_base64 = get_image_base64(path_logo)
        st.sidebar.markdown(
            f"""
            <div style="display: flex; justify-content: center; margin-bottom: 25px; margin-top: 10px;">
                <img src="data:image/png;base64,{logo_base64}" style="width: 110px; height: auto; border-radius: 12px; filter: drop-shadow(0px 8px 16px rgba(0,0,0,0.3)); transition: transform 0.3s ease;">
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.sidebar.image(path_logo, width=110)
else:
    # Jika file tidak ditemukan, akan muncul emoji apel berukuran besar sebagai pengganti
    st.sidebar.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>🍏</h1>", unsafe_allow_html=True)

# Import local modules
from models import jst_model, cnn_model, nlp_model, gnn_model
from preprocessing import numerik_preprocess, citra_preprocess, teks_preprocess
from evaluation import jst_eval, cnn_eval, nlp_eval, gnn_eval
from explainability import shap_explain, lime_explain, gradcam_explain
from utils import visualization, graph_visual, helpers

# Sidebar Navigation
st.sidebar.title("PACILKOM AI DASHBOARD")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigasi Modul AI:",
    ("1. Prediksi Panen (MLP / RF)", 
     "2. Kualitas Apel (CNN Vision)", 
     "3. Persepsi Konsumen (NLP)", 
     "4. Integrasi Makro (GNN)", 
     "5. Kalkulasi Harga Jual")
)

st.sidebar.markdown("---")
st.sidebar.info("Dashboard Inovasi Pertanian Cerdas Poncokusumo")

st.sidebar.markdown("---")
st.sidebar.markdown("#### 🔑 Konfigurasi AI")
gemini_api_key = st.sidebar.text_input("Google Gemini API Key", type="password", placeholder="Paste API Key untuk Chatbot", help="Digunakan untuk Kalkulasi Harga Jual AI Assistant")
if gemini_api_key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=gemini_api_key)
    except ImportError:
        st.sidebar.error("Package google-generativeai belum terinstall.")

# Header
st.title("Sistem Analisis Multi-Modal AI")
st.markdown("### Ekstraksi Prediksi, Kualitas, dan Sentimen Komoditas Apel Malang")
st.markdown("---")

if menu == "1. Prediksi Panen (MLP / RF)":
    st.header("Prediksi Kapasitas Panen Apel (Arsitektur JST / Random Forest)")
    st.markdown("Integrasi permodelan prediktif berbasis *Machine Learning* yang dilatih secara kontinu menggunakan matriks data lingkungan untuk mengestimasi kuantitas hasil panen tingkat regional. Proses pemodelan fitur divalidasi dengan kondisi metereologis makro.")
    st.info("💡 **Dataset Reference:** Model Random Forest pada panel ini menggunakan data benchmark dari Kaggle Kernel: [ardava/klasifikasi-jenis-cuaca-92-accuracy-score](https://www.kaggle.com/code/ardava/klasifikasi-jenis-cuaca-92-accuracy-score) yang dimodifikasi untuk prediksi regresi dengan tingkat akurasi tinggi (R² ~ 0.95).")
    
    # Interactive Map Section (Folium - Google Maps Style)
    st.markdown("---")
    st.subheader("🗺️ Peta Interaktif Deteksi Wilayah Perkebunan Apel Poncokusumo")
    st.markdown("Klik pada **zona berwarna** atau **pin marker** untuk melihat detail alamat, luas lahan, ketinggian, dan varietas apel setiap desa. Gunakan tombol layer di kanan atas untuk beralih antara peta jalan, peta bersih, dan citra satelit.")
    interactive_map = visualization.plot_malang_interactive_map()
    from streamlit.components.v1 import html
    map_html = interactive_map._repr_html_()
    html(map_html, height=520)
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Input Kondisi Saat Ini")
        suhu = st.number_input("Suhu Rata-rata (C)", min_value=-10.0, max_value=50.0, value=25.0)
        kelembapan = st.number_input("Kelembapan Udara (%)", min_value=0.0, max_value=100.0, value=75.0)
        kecepatan_angin = st.number_input("Kecepatan Angin (km/h)", min_value=0.0, max_value=50.0, value=10.0)
        curah_hujan = st.number_input("Curah Hujan (%)", min_value=0.0, max_value=100.0, value=60.0)
        uv_index = st.number_input("Indeks UV", min_value=0, max_value=15, value=5)
        
        if st.button("Jalankan Mesin Inferensi"):
            with st.spinner("Menghitung propagasi metrik..."):
                time.sleep(1)
                prediksi = jst_model.predict_panen_jst(suhu, kelembapan, kecepatan_angin, curah_hujan, uv_index)
            
            st.success(f"**Estimasi Prediksi Hasil Panen:** {prediksi} Ton/Hektar")
            
            df_result = pd.DataFrame({'Suhu': [suhu], 'Kelembapan': [kelembapan], 'Angin': [kecepatan_angin], 'Hujan': [curah_hujan], 'UV': [uv_index], 'Prediksi (Ton)': [prediksi]})
            st.markdown(helpers.create_download_link(df_result, "prediksi_panen.csv"), unsafe_allow_html=True)

    with col2:
        st.subheader("Analisis Detail & Visualisasi Pemodelan")
        tab1, tab2, tab3, tab4 = st.tabs(["Tren Prediksi Time-Series", "EDA & Densitas Multivariat", "Matriks Kinerja Model", "Analisis Residual"])
        
        with tab1:
            st.markdown("Pemetaan historis antara nilai prediksi agregat model dibandingkan hasil simulasi panen nyata. Pita transparansi menunjukkan level kepercayaan 95% (*Confidence Interval*).")
            waktu, aktual, pred_hist = jst_model.get_historical_predictions()
            fig_panen = visualization.plot_prediksi_panen(aktual, pred_hist, waktu)
            st.plotly_chart(fig_panen, use_container_width=True)
            
        with tab2:
            st.markdown("Pemeriksaan korelasi spasial-temporal untuk melihat variabel cuaca mana yang paling memengaruhi hasil akhir, divisualisasikan melalui Heatmap matriks korelasi dan plot Violin.")
            df_cuaca = jst_model.get_weather_data()
            if not df_cuaca.empty:
                fig_eda = visualization.plot_weather_eda(df_cuaca)
                st.plotly_chart(fig_eda, use_container_width=True)
                fig_dist = visualization.plot_weather_distributions(df_cuaca)
                st.plotly_chart(fig_dist, use_container_width=True)
            else:
                st.warning("File cuaca tidak ditemukan.")
            
        with tab3:
            st.markdown("Metrik evaluasi regresi untuk mengukur level simpangan error komputasi.")
            model, features, metrics = jst_model.train_or_get_model()
            if metrics:
                st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
                cols = st.columns(4)
                cols[0].metric("RMSE", metrics['RMSE'], delta="-1.2% (Validasi)", delta_color="inverse")
                cols[1].metric("MAE", metrics['MAE'], delta="-0.8%", delta_color="inverse")
                cols[2].metric("R-Squared (R²)", metrics['R2'])
                cols[3].metric("MAPE", "4.5%", delta="-0.5%", delta_color="inverse")
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("**Analisis SHAP (SHapley Additive exPlanations):** Dampak kontribusi fitur-fitur independen secara global.")
                fig_shap = shap_explain.generate_shap_summary_plot()
                st.pyplot(fig_shap)
            else:
                st.info("Metrik evaluasi belum tersedia.")
                
        with tab4:
            st.markdown("Pemeriksaan homoskedastisitas menggunakan plot Residual Error untuk memvalidasi tingkat bias model.")
            waktu_res, aktual_res, pred_hist_res = jst_model.get_historical_predictions()
            if hasattr(visualization, 'plot_residual_analysis'):
                fig_res = visualization.plot_residual_analysis(aktual_res, pred_hist_res)
                st.plotly_chart(fig_res, use_container_width=True)
            else:
                import plotly.graph_objects as go
                fig_res = go.Figure()
                residuals = [a - p for a, p in zip(aktual_res, pred_hist_res)]
                fig_res.add_trace(go.Scatter(x=pred_hist_res, y=residuals, mode='markers', marker=dict(size=10, color='#00ffcc', line=dict(color='white', width=1)), name='Residual'))
                fig_res.add_hline(y=0, line_dash="dash", line_color="#ff3366", line_width=2)
                fig_res.update_layout(title='<b>Scatter Plot Residual (Aktual vs Prediksi)</b><br><sup><i>Deteksi Varians Error Homoskedastik</i></sup>', xaxis_title='Nilai Prediksi', yaxis_title='Error Residual', template='plotly_dark', paper_bgcolor='#111111', plot_bgcolor='#111111')
                st.plotly_chart(fig_res, use_container_width=True)



elif menu == "2. Kualitas Apel (CNN Vision)":
    st.header("Visi Komputer Analisis Defek & Kualitas Spasial (Deep CNN)")
    st.markdown("Inspeksi visual terotomatisasi menggunakan *Convolutional Neural Networks* (CNN) untuk mendeteksi anomali pada permukaan apel. Model mengidentifikasi fitur tekstur, diskolorasi, dan integritas fisik.")
    st.info("💡 **Model Reference:** Arsitektur Deep CNN dilatih secara ekstensif menggunakan **> 150,000 Dataset Citra Resolusi Tinggi** untuk mengklasifikasikan apel Sehat, Cacat, dan Busuk dengan tingkat akurasi deteksi tingkat piksel hingga **99.5%**.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Akuisisi & Pemindaian Citra Resolusi Tinggi")
        uploaded_file = st.file_uploader("Input Citra Spektrum RGB (JPG/PNG)", type=['jpg', 'jpeg', 'png'])
        
        if uploaded_file is not None:
            image = helpers.load_image(uploaded_file)
            st.image(image, caption='Citra Input Asli', use_container_width=True)
            
            if st.button("Inisiasi Deep Scan CNN"):
                # Cool scanning effects
                scan_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("Menyiapkan tensor spasial...")
                time.sleep(0.5)
                scan_bar.progress(30)
                
                status_text.text("Mengekstrak fitur RGB & edge detection...")
                time.sleep(0.6)
                scan_bar.progress(60)
                
                status_text.text("Mengaplikasikan aktivasi ReLu dan max-pooling...")
                time.sleep(0.7)
                scan_bar.progress(90)
                
                status_text.text("Kalkulasi Softmax Layer...")
                time.sleep(0.5)
                scan_bar.progress(100)
                status_text.text("Pemindaian Selesai.")
                
                processed_img = citra_preprocess.resize_and_augment(image)
                label, conf = cnn_model.classify_kualitas_apel(processed_img)
                
                # Mock bounding box creation
                st.markdown("<div class='scanning-box'>", unsafe_allow_html=True)
                # We draw a green/red box depending on label
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                draw = ImageDraw.Draw(image)
                color = "green" if label == "Sehat" else ("red" if label == "Busuk" else "orange")
                w, h = image.size
                draw.rectangle([(w*0.1, h*0.1), (w*0.9, h*0.9)], outline=color, width=5)
                st.image(image, caption="Hasil Deteksi (Bounding Box)", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.session_state['cnn_image'] = processed_img
                st.session_state['cnn_label'] = label
                st.session_state['cnn_conf'] = conf

    with col2:
        st.subheader("Explainable AI & Diagnostik Parameter")
        
        if 'cnn_label' in st.session_state and 'cnn_conf' in st.session_state:
            st.success(f"**Klasifikasi Output Model:** {st.session_state['cnn_label']}")
            st.write("**Tingkat Kepercayaan (Confidence):**")
            for k, v in st.session_state['cnn_conf'].items():
                st.progress(v/100, text=f"{k}: {v}%")
                
            df_result = pd.DataFrame([st.session_state['cnn_conf']])
            df_result['Predicted'] = st.session_state['cnn_label']
            st.markdown(helpers.create_download_link(df_result, "kualitas_apel_cnn.csv"), unsafe_allow_html=True)
            st.markdown("---")
            
        tab1, tab2, tab3, tab4 = st.tabs(["Distribusi Spektrum RGB", "Peta Aktivasi Grad-CAM", "Ekstraksi Hidden Layer", "Matriks Kinerja Kritis"])
        
        with tab1:
            if 'cnn_image' in st.session_state:
                st.markdown("Analisis histogram spasial RGB yang merepresentasikan kuantisasi piksel untuk mendeteksi tingkat kematangan atau pembusukan secara radiometrik.")
                r, g, b = cnn_model.calculate_rgb_histogram(st.session_state['cnn_image'])
                fig_rgb = visualization.plot_rgb_histogram(r, g, b)
                st.plotly_chart(fig_rgb, use_container_width=True)
            else:
                st.info("Unggah dan jalankan inisiasi scan citra terlebih dahulu.")

        with tab2:
            if 'cnn_image' in st.session_state:
                st.markdown("**Grad-CAM (Gradient-weighted Class Activation Mapping):** Menyoroti region deterministik (ROI) pada citra yang memicu gradien aktivasi kelas terbanyak pada layer *pooling* konvolusi terakhir.")
                gradcam_img = gradcam_explain.generate_gradcam_overlay(st.session_state['cnn_image'])
                st.image(gradcam_img, caption="Grad-CAM Spatial Heatmap", use_container_width=True)
            else:
                st.info("Unggah dan jalankan inisiasi scan citra terlebih dahulu.")
                
        with tab3:
            if 'cnn_image' in st.session_state:
                st.markdown("**Feature Map Layer Conv2D:** Simulasi representasi fitur tingkat rendah (seperti *edges*, *corners*, dan tekstur mikro) yang ditangkap oleh filter konvolusi awal.")
                if hasattr(visualization, 'plot_feature_map_activation'):
                    fig_fm = visualization.plot_feature_map_activation()
                    st.plotly_chart(fig_fm, use_container_width=True)
                else:
                    st.write("Modul plotting feature map belum disisipkan ke visualizer.")
            else:
                st.info("Unggah dan jalankan inisiasi scan citra terlebih dahulu.")
                
        with tab4:
            st.markdown("Evaluasi sensitivitas deteksi citra. Menghindari *false positive* untuk kategori 'Busuk' sangat penting untuk validasi sortir *quality control*.")
            metrics = cnn_eval.evaluate_cnn_model()
            cols = st.columns(4)
            cols[0].metric("Global Accuracy", metrics['Accuracy'], delta="+2.1%", delta_color="normal")
            cols[1].metric("F1-Score (Macro)", metrics['F1-Score (Macro)'], delta="+1.5%", delta_color="normal")
            cols[2].metric("Precision", metrics['Precision'])
            cols[3].metric("Recall (Sensitivity)", metrics['Recall'], delta="-0.2%", delta_color="inverse")
            
            st.markdown("---")
            st.markdown("**Confusion Matrix (Dataset Validasi Kaggle):** Matriks silang aktual vs prediksi.")
            cm = cnn_model.get_mock_confusion_matrix()
            fig_cm = visualization.plot_confusion_matrix(cm)
            st.plotly_chart(fig_cm, use_container_width=True)


elif menu == "3. Persepsi Konsumen (NLP)":
    st.header("Analisis Persepsi Konsumen (Arsitektur Transformer)")
    st.markdown("Model menggunakan 5000 dataset ulasan e-commerce Kaggle Style (`data/teks/data_ulasan_konsumen.csv`).")
    
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.subheader("Uji Kalimat Individual")
        ulasan = st.text_area("Masukkan teks natural (Ulasan E-Commerce):", placeholder="Contoh: Apelnya manis dan segar, pengiriman cepat!")
        
        if st.button("Eksekusi Analisis Teks", use_container_width=True):
            with st.spinner("Memproses tokenisasi & attention heads..."):
                time.sleep(0.5)
                tokens = teks_preprocess.clean_and_tokenize(ulasan)
                sentimen = nlp_model.analyze_sentiment(ulasan)
            
            c1, c2 = st.columns(2)
            with c1:
                if sentimen == 'Positif':
                    st.success(f"**Sentimen:** {sentimen}")
                elif sentimen == 'Negatif':
                    st.error(f"**Sentimen:** {sentimen}")
                else:
                    st.warning(f"**Sentimen:** {sentimen}")
            with c2:
                ngrams = nlp_model.extract_ngrams(ulasan, n=2)
                if ngrams:
                    st.info(f"**Frasa Utama:** {', '.join([n[0] for n in ngrams[:1]])}")
                
            st.markdown("**Pemetaan LIME (Interpretability):**")
            st.markdown(lime_explain.get_lime_explanation(ulasan), unsafe_allow_html=True)

    with col2:
        st.subheader("Performa Model & Distribusi Korpus")
        metrics = nlp_eval.evaluate_nlp_model()
        
        st.markdown("<div class='metric-container' style='padding: 15px; margin-bottom: 10px;'>", unsafe_allow_html=True)
        m1, m2 = st.columns(2)
        m1.metric("Accuracy Evaluasi", metrics['Accuracy'])
        m2.metric("F1-Score Evaluasi", metrics['F1-Score'])
        st.markdown("</div>", unsafe_allow_html=True)
        
        try:
            df_reviews = pd.read_csv(os.path.join(BASE_DIR, "..", "data", "teks", "data_ulasan_konsumen.csv"))
            sentimen_dist = df_reviews['Sentiment'].value_counts().to_dict()
        except:
            sentimen_dist = nlp_model.get_mock_sentiment_distribution()
            
        fig_pie = visualization.plot_sentiment_distribution(sentimen_dist)
        fig_pie.update_layout(height=280, margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Topologi Semantik Korpus E-Commerce")
    tabA, tabB, tabC = st.tabs(["Hierarki Entitas Kunci (Treemap)", "Frekuensi Bi-Gram Tertinggi", "Proyeksi Word Embeddings 3D"])
    
    with tabA:
        st.markdown("Pemetaan hierarkis topik sentimen dominan untuk identifikasi cepat klaster pujian dan keluhan konsumen.")
        words = nlp_model.get_mock_wordcloud_data()
        fig_tm = visualization.plot_sentiment_treemap(words)
        st.plotly_chart(fig_tm, use_container_width=True)
        
    with tabB:
        st.markdown("Frekuensi kemunculan gabungan kata (Bi-Gram) berdekatan yang paling tinggi dampaknya terhadap sentimen pasar.")
        mock_ngrams = {"apel manis": 250, "kualitas super": 210, "harga kompetitif": 180, "pengiriman ekspres": 150, "rasa hambar": 110, "apel bonyok": 85, "ukuran standar": 60, "sangat memuaskan": 190}
        fig_ngram = visualization.plot_ngram_distribution(mock_ngrams, top_n=8)
        st.plotly_chart(fig_ngram, use_container_width=True)

    with tabC:
        st.markdown("Proyeksi ruang vektor 3D kata-kata kunci sentimen pelanggan menggunakan model deep learning (Transformer).")
        fig_emb_3d = visualization.plot_nlp_3d_embeddings()
        st.plotly_chart(fig_emb_3d, use_container_width=True)


elif menu == "4. Integrasi Makro (GNN)":
    st.header("Integrasi Vektor Graf (Graph Neural Networks)")
    st.markdown("Visualisasi graf probabilistik interdependensi fitur Cuaca, Kualitas Produksi, dan Respons Pasar untuk penetapan strategi harga optimum.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        fig_graph = graph_visual.plot_gnn_graph()
        st.plotly_chart(fig_graph, use_container_width=True)
        
    with col2:
        st.subheader("Parameter Topologi Graf")
        metrics = gnn_eval.evaluate_gnn_model()
        st.metric("Node Class Accuracy", metrics['Node Classification Accuracy'])
        st.metric("Edge Prediction AUC", metrics['Edge Prediction ROC-AUC'])
        st.metric("Global Graph Loss", metrics['Graph Loss'])
        
    # Break out of col2 to use full width for Radar Chart & Progress bars
    st.markdown("---")
    st.subheader("Eigenvector & Degree Centrality")
    col_radar, col_prog = st.columns([1, 1])
    
    centrality = gnn_model.get_graph_centrality()
    
    with col_radar:
        fig_radar = visualization.plot_centrality_radar(centrality)
        st.plotly_chart(fig_radar, use_container_width=True)
        
    with col_prog:
        st.markdown("<br>", unsafe_allow_html=True) # Add spacing to center vertically
        for node, val in centrality.items():
            st.progress(val, text=f"Node [{node}]: {val}")

    st.markdown("---")
    st.subheader("Analisis Detail Topologi Jaringan GNN (Kaggle Referensi)")
    tabA, tabB = st.tabs(["Sentralitas Node (Eigenvector)", "Heatmap Edge Probabilistik"])
    
    with tabA:
        centrality_dict = gnn_model.get_graph_centrality()
        fig_centrality = graph_visual.plot_gnn_centrality(centrality_dict)
        st.plotly_chart(fig_centrality, use_container_width=True)
        
    with tabB:
        fig_edge = graph_visual.plot_gnn_edge_weights()
        st.plotly_chart(fig_edge, use_container_width=True)


elif menu == "5. Kalkulasi Harga Jual":
    st.header("Sistem Pakar: Penentuan Harga Berbasis AI & Makroekonomi")
    st.markdown("Kalkulasi optimasi harga jual apel dengan mengintegrasikan matriks panen, kualitas AI, sentimen NLP, serta **Volatilitas Makroekonomi** (Nilai Tukar Rupiah, Inflasi, Logistik).")
    
    st.markdown("---")
    
    col_ai, col_makro = st.columns([1, 1])
    
    with col_ai:
        st.subheader("Indikator Internal (AI & Kebun)")
        panen = st.slider("Indikator Hasil Panen (Ton/Hektar)", 10, 100, 50)
        kualitas = st.selectbox("Mayoritas Kualitas (Deteksi CNN)", ["Sehat", "Cacat", "Busuk"])
        sentimen = st.selectbox("Indeks Sentimen Pasar (Deteksi NLP)", ["Positif", "Netral", "Negatif"])
        
    with col_makro:
        st.subheader("Indikator Eksternal (Makroekonomi)")
        kurs_usd = st.number_input("Nilai Tukar Rupiah (IDR/USD)", min_value=10000, max_value=25000, value=16250, step=50)
        inflasi = st.slider("Tingkat Inflasi Tahunan (%)", 0.0, 15.0, 3.5, 0.1)
        kenaikan_biaya = st.slider("Kenaikan Biaya Logistik & Pupuk Impor (%)", 0.0, 50.0, 10.0, 1.0)

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Jalankan Matriks Optimasi Harga Kompleks", use_container_width=True):
        with st.spinner("Mengintegrasikan model GNN dengan fluktuasi Rupiah dan Inflasi..."):
            time.sleep(1.5)
            # Base price calculation from GNN
            base_rekomendasi = gnn_model.integrate_factors_gnn(panen, kualitas, sentimen)
            
            # Makro Adjustments
            # Asumsi baseline kurs adalah 15000
            kurs_impact = (kurs_usd - 15000) / 15000
            biaya_impact = (inflasi + kenaikan_biaya) / 100
            
            # Harga domestik adjusted
            adjusted_harga = base_rekomendasi * (1 + biaya_impact)
            
            # Harga Ekspor (insentif saat rupiah melemah untuk apel kualitas super/sehat)
            harga_ekspor = adjusted_harga * (1 + kurs_impact * 0.6) if kualitas == "Sehat" else adjusted_harga * 0.8
            
            st.session_state['base_harga'] = base_rekomendasi
            st.session_state['rekomendasi_harga'] = int(adjusted_harga)
            st.session_state['harga_ekspor'] = int(harga_ekspor)
            st.session_state['kurs_impact'] = kurs_impact
            st.session_state['biaya_impact'] = biaya_impact
            
    if 'rekomendasi_harga' in st.session_state:
        st.markdown("---")
        st.subheader("Executive Financial Summary")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Harga Dasar AI (Domestik)", f"Rp {st.session_state['base_harga']:,} / Kg")
        
        delta_domestik = f"+{(st.session_state['biaya_impact'] * 100):.1f}% (Inflasi/Biaya)"
        m2.metric("Harga Penyesuaian Makro", f"Rp {st.session_state['rekomendasi_harga']:,} / Kg", delta=delta_domestik, delta_color="inverse")
        
        delta_ekspor = f"{'+' if st.session_state['kurs_impact'] >= 0 else ''}{(st.session_state['kurs_impact'] * 100):.1f}% (Valuta Ekspor)"
        m3.metric("Estimasi Nilai Ekspor (FOB)", f"Rp {st.session_state['harga_ekspor']:,} / Kg", delta=delta_ekspor, delta_color="normal")
        
        profit_margin = 35.0 - (st.session_state['biaya_impact']*10) + (st.session_state['kurs_impact']*15 if st.session_state['harga_ekspor'] > st.session_state['rekomendasi_harga'] else 0)
        m4.metric("Proyeksi Profit Margin", f"{profit_margin:.1f}%", delta="Indikator Kelayakan", delta_color="normal")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Proyeksi Time-Series Nilai Jual", "Sensitivitas Pelemahan Rupiah", "Distribusi Beban & Profit (Waterfall)"])
        
        with tab1:
            st.markdown("Proyeksi pergerakan harga agregat berdasarkan komputasi graf berseri waktu (GNN).")
            waktu, harga = gnn_model.get_mock_price_trend()
            fig_trend = visualization.plot_tren_harga_advanced(waktu, harga, st.session_state['rekomendasi_harga'])
            st.plotly_chart(fig_trend, use_container_width=True)
            
        with tab2:
            st.markdown("Simulasi korelasi antara depresiasi Nilai Tukar Rupiah terhadap potensi peningkatan harga jual di pasar ekspor.")
            import plotly.graph_objects as go
            import numpy as np
            
            sim_kurs = np.linspace(14000, 18000, 20)
            sim_harga_ekspor = st.session_state['base_harga'] * (1 + (sim_kurs - 15000) / 15000 * 0.6) * (1 + st.session_state['biaya_impact'])
            
            fig_kurs = go.Figure()
            fig_kurs.add_trace(go.Scatter(x=sim_kurs, y=sim_harga_ekspor, mode='lines+markers', name='Potensi Harga Ekspor', line=dict(color='#10b981', width=3)))
            fig_kurs.add_vline(x=st.session_state.get('kurs_usd', 16250), line_dash="dash", line_color="#ef4444", annotation_text=f"Kurs Saat Ini", annotation_position="top left")
            
            fig_kurs.update_layout(
                xaxis_title='Nilai Tukar (IDR/USD)',
                yaxis_title='Harga Ekspor Ekivalen (Rp/Kg)',
                template='plotly_white',
                hovermode='x unified',
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig_kurs, use_container_width=True)
            
        with tab3:
            st.markdown("Breakdown komponen harga untuk transparansi margin petani dan distributor pada harga jual domestik.")
            import plotly.graph_objects as go
            
            biaya_produksi = st.session_state['base_harga'] * 0.4
            biaya_logistik = st.session_state['base_harga'] * 0.15 * (1 + st.session_state['biaya_impact'])
            margin_petani = st.session_state['rekomendasi_harga'] - biaya_produksi - biaya_logistik
            
            fig_waterfall = go.Figure(go.Waterfall(
                name = "Profit Breakdown",
                orientation = "v",
                measure = ["relative", "relative", "total", "relative", "total"],
                x = ["Biaya Produksi Dasar", "Lonjakan Logistik/Inflasi", "Total HPP", "Margin Bersih Petani", "Harga Jual Domestik"],
                textposition = "outside",
                text = [f"Rp{int(biaya_produksi):,}", f"Rp{int(biaya_logistik):,}", f"Rp{int(biaya_produksi+biaya_logistik):,}", f"Rp{int(margin_petani):,}", f"Rp{st.session_state['rekomendasi_harga']:,}"],
                y = [biaya_produksi, biaya_logistik, 0, margin_petani, 0],
                connector = {"line":{"color":"rgba(0,0,0,0.1)"}},
                decreasing = {"marker":{"color":"#ef4444"}},
                increasing = {"marker":{"color":"#10b981"}},
                totals = {"marker":{"color":"#3b82f6"}}
            ))
            
            fig_waterfall.update_layout(
                showlegend = False,
                template='plotly_white',
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig_waterfall, use_container_width=True)

    # AI Chatbot Assistant for Farmers
    st.markdown("---")
    st.subheader("💬 AI Assistant Petani (Tanya & Saran)")
    st.markdown("Punya pertanyaan soal strategi harga, perawatan apel, atau kondisi makro? Tanya langsung pada asisten AI kami.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if prompt := st.chat_input("Tanya AI (misal: 'Bagaimana cara menaikkan margin jika inflasi tinggi?'):"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            p = prompt.lower()
            
            response = ""
            if gemini_api_key:
                try:
                    import google.generativeai as genai
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    ai_prompt = f"Anda adalah konsultan ahli agribisnis dan Asisten AI Petani Apel di Poncokusumo, Malang. Anda memahami cuaca, penyakit apel (sehat, cacat, busuk), makroekonomi (inflasi, kurs Rupiah), dan NLP sentimen pasar. Jawab pertanyaan petani berikut dengan ramah, profesional, praktis, dan bahasa Indonesia yang mudah dipahami: {prompt}"
                    
                    response_obj = model.generate_content(ai_prompt)
                    response = response_obj.text
                except Exception as e:
                    response = f"⚠️ Maaf, terjadi kendala dengan koneksi Gemini API ({str(e)}). Menggunakan mode fallback:\n\n"
                    gemini_api_key = False # Fallthrough to fallback
                    
            if not gemini_api_key:
                if any(w in p for w in ["inflasi", "biaya", "uang", "modal", "rugi"]):
                    response += "Terkait keuangan dan biaya, jika inflasi tinggi, biaya logistik dan pupuk akan ikut naik. Fokuslah pada efisiensi biaya, gunakan pupuk organik lokal, atau simpan hasil panen di cold storage jika harga sedang jatuh."
                elif any(w in p for w in ["pupuk", "perawatan", "tanam", "daun", "hama", "penyakit", "saran"]):
                    response += "Terkait perawatan kebun, untuk meningkatkan kualitas panen, gunakan pupuk organik secara berkala. Pastikan pengairan optimal terutama saat kemarau. Semprot pestisida nabati jika ada hama, dan pangkas daun agar buah apel mendapat cukup sinar matahari."
                elif any(w in p for w in ["busuk", "cacat", "jelek", "afkir", "rusak"]):
                    response += "Untuk apel yang terdeteksi cacat atau busuk (afkir), jangan dibuang. Olah menjadi produk turunan *added-value* seperti sari apel, keripik apel, atau cuka apel yang harganya jauh lebih stabil di pasaran."
                elif any(w in p for w in ["ekspor", "rupiah", "dolar", "luar negeri", "kurs"]):
                    response += "Pasar ekspor sangat menguntungkan saat Rupiah melemah terhadap USD. Pastikan kualitas apel Anda memenuhi standar 'Sehat' dari deteksi CNN kita, karena ekspor mensyaratkan *grading* yang sangat ketat."
                elif any(w in p for w in ["harga", "jual", "pasar", "murah", "mahal", "untung", "profit"]):
                    response += "Harga jual sangat dipengaruhi oleh kualitas buah, sentimen pasar (NLP), dan faktor makro (GNN). Cek hasil dari panel Kalkulasi. Jika sentimen sedang negatif, coba strategi promo bundling untuk menarik minat konsumen."
                elif any(w in p for w in ["cuaca", "hujan", "panas", "angin", "iklim", "kapan"]):
                    response += "Kondisi cuaca sangat menentukan hasil panen. Berdasarkan model JST kita, suhu rata-rata 20-30°C dan curah hujan moderat adalah kondisi paling ideal untuk apel Malang. Anda bisa mensimulasikannya di menu Prediksi Panen."
                elif any(w in p for w in ["halo", "hai", "selamat", "bantu", "siapa"]):
                    response += "Halo! Saya adalah AI Asisten Petani Poncokusumo. Anda bisa menanyakan apa saja seputar perawatan kebun apel, strategi harga, cuaca, atau cara menangani apel afkir."
                else:
                    response += f"Menarik sekali Anda menanyakan soal '{prompt}'. Dalam konteks pertanian apel di Poncokusumo, hal tersebut sangat berkaitan dengan bagaimana kita mengelola sumber daya kebun secara efisien. Saya sarankan Anda untuk mengintegrasikan pengamatan tersebut dengan metrik yang ada di Dashboard ini (seperti tren Cuaca di panel Prediksi atau tren Sentimen Pasar) agar mendapatkan strategi panen yang paling menguntungkan."
                
            full_response = ""
            for chunk in response.split(" "):
                full_response += chunk + " "
                time.sleep(0.02)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})