from PIL import Image

def resize_and_augment(image):
    """Simulasi augmentasi dan resize citra."""
    if isinstance(image, Image.Image):
        # Resize standard for CNN (e.g. 224x224)
        return image.resize((224, 224))
    return image
