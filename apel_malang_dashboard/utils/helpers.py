import base64
from PIL import Image
import io

def load_image(image_file):
    """Load uploaded image."""
    img = Image.open(image_file)
    return img

def get_base64_of_bin_file(bin_file):
    """Read binary file and return base64 string."""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def create_download_link(data_df, filename="hasil_analisis.csv", link_text="📥 Download Hasil Analisis (CSV)"):
    """Create a download link for dataframe."""
    csv = data_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" class="download-button">{link_text}</a>'
    return href
