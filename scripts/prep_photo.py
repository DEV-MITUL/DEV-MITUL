import sys
import os
from PIL import Image, ImageEnhance, ImageOps, ImageDraw
import numpy as np

def generate_fallback_hero(path="hero.png"):
    """Generates a stylized synthetic hero portrait if no input file exists."""
    width, height = 300, 360
    img = Image.new("RGBA", (width, height), (13, 13, 13, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw background radial lighting
    for r in range(180, 0, -2):
        alpha = int(255 * (1 - (r / 180)))
        gold_color = (212, 175, 55, int(alpha * 0.35))
        draw.ellipse([width//2 - r, height//2 - r, width//2 + r, height//2 + r], fill=gold_color)
    
    # Draw head outline & shoulders silhouette
    draw.ellipse([width//2 - 65, 50, width//2 + 65, 190], fill=(220, 220, 230, 255)) # Head
    draw.polygon([
        (width//2 - 110, height),
        (width//2 - 70, 185),
        (width//2 + 70, 185),
        (width//2 + 110, height)
    ], fill=(180, 180, 190, 255)) # Shoulders

    # Eyes & details for contrast
    draw.ellipse([width//2 - 35, 110, width//2 - 15, 125], fill=(20, 20, 20, 255))
    draw.ellipse([width//2 + 15, 110, width//2 + 35, 125], fill=(20, 20, 20, 255))
    draw.rectangle([width//2 - 25, 150, width//2 + 25, 160], fill=(40, 40, 40, 255))
    
    img.save(path)
    print(f"[+] Created synthetic starter portrait at '{path}'")

def prep_photo(input_path="prompt2_img.png", output_path="source-prepped.png"):
    print(f"[*] Processing photo: {input_path}")
    if not os.path.exists(input_path):
        print(f"[!] Input image '{input_path}' not found. Generating default avatar...")
        generate_fallback_hero(input_path)

    try:
        img = Image.open(input_path).convert("RGBA")
    except Exception as e:
        print(f"[!] Error opening image {input_path}: {e}")
        generate_fallback_hero(input_path)
        img = Image.open(input_path).convert("RGBA")

    # Background Isolation & Enhancement
    try:
        # Fast local dark background contrast isolator
        np_img = np.array(img)
        if img.mode == "RGBA":
            alpha = np_img[:, :, 3]
            mask = alpha > 30
        else:
            # Luminance masking for dark/neon cyber background
            luma = 0.299 * np_img[:, :, 0] + 0.587 * np_img[:, :, 1] + 0.114 * np_img[:, :, 2]
            mask = luma > 15
        
        # Apply mask
        np_img[~mask] = [13, 13, 13, 255] if img.mode == "RGBA" else [13, 13, 13]
        output = Image.fromarray(np_img)
    except Exception as e:
        print(f"[!] Standard isolator fallback: {e}")
        output = img

    # Paste onto sleek terminal dark background (#0d0d0d)
    bg = Image.new("RGB", output.size, (13, 13, 13))
    if output.mode == "RGBA":
        bg.paste(output, mask=output.split()[3])
    else:
        bg.paste(output)
    
    # Contrast Enhancement (CLAHE with OpenCV if present, fallback to PIL)
    try:
        import cv2
        np_bg = np.array(bg)
        lab = cv2.cvtColor(np_bg, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.5, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        enhanced_np = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)
        final_img = Image.fromarray(enhanced_np)
        print("[*] CLAHE contrast enhancement applied.")
    except Exception as e:
        print(f"[*] Applying PIL contrast enhancement ({e})...")
        enhancer = ImageEnhance.Contrast(bg)
        final_img = enhancer.enhance(1.4)

    # Crop & Resize to standard 100x120 aspect ratio for ASCII matrix
    target_w, target_h = 100, 120
    final_img = ImageOps.fit(final_img, (target_w, target_h), method=Image.Resampling.LANCZOS)
    
    final_img.save(output_path)
    print(f"[OK] Saved source-prepped image to '{output_path}' ({target_w}x{target_h})")

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "hero.png"
    prep_photo(input_file)
