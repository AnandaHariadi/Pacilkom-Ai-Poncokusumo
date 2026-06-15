from PIL import Image, ImageDraw
import random

def generate_gradcam_overlay(image):
    """Membuat mock Grad-CAM overlay pada gambar (hanya mock visual)."""
    if isinstance(image, Image.Image):
        # Create a red/yellow overlay ellipse
        overlay = image.copy()
        draw = ImageDraw.Draw(overlay, 'RGBA')
        width, height = overlay.size
        
        # Random location for the heatmap 'hotspot'
        cx = random.randint(int(width*0.3), int(width*0.7))
        cy = random.randint(int(height*0.3), int(height*0.7))
        r = min(width, height) * 0.3
        
        draw.ellipse((cx-r, cy-r, cx+r, cy+r), fill=(255, 0, 0, 100))
        draw.ellipse((cx-r*0.6, cy-r*0.6, cx+r*0.6, cy+r*0.6), fill=(255, 255, 0, 150))
        
        return overlay
    return image
