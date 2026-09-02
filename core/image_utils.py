import os
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

def convert_to_webp(image_field, quality=85):
    """
    Automatically converts uploaded ImageField files to lightweight .webp format.
    Enhances multimedia loading speed across the site while maintaining high quality.
    """
    if not image_field or not hasattr(image_field, 'file'):
        return

    filename_base = os.path.splitext(os.path.basename(image_field.name))[0]
    
    # Skip if already webp
    if image_field.name.lower().endswith('.webp'):
        return

    try:
        img = Image.open(image_field.file)
        
        # Preserve transparency for PNGs / RGBA images
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")

        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=quality, optimize=True)
        buffer.seek(0)

        new_filename = f"{filename_base}.webp"
        image_field.save(new_filename, ContentFile(buffer.read()), save=False)
    except Exception:
        # If conversion encounters non-image/corrupt data, retain original gracefully
        pass
