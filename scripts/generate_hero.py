import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def generate_tech_emblem_hero(output_path="hero.png"):
    """
    Generates a sleek 3D metallic tech emblem graphic for hero.png
    featuring a stylized interlocking 'M' & 'D' cyber crest, gold rim lighting,
    and dark charcoal concentric HUD rings.
    """
    width, height = 600, 720
    img = Image.new("RGBA", (width, height), (13, 13, 13, 255))
    draw = ImageDraw.Draw(img)

    cx, cy = width // 2, height // 2

    # 1. Ambient Gold Radial Backlight Glow
    for r in range(320, 0, -2):
        alpha = int(240 * (1 - (r / 320)))
        color = (212, 175, 55, int(alpha * 0.38))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

    # 2. Concentric Tech Target HUD Rings
    for r, w, color in [
        (280, 1.5, (0, 255, 204, 30)),
        (240, 2, (212, 175, 55, 60)),
        (200, 1.5, (0, 255, 204, 40)),
        (160, 2, (212, 175, 55, 80))
    ]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=int(w))

    # Crosshair HUD ticks
    draw.line([(cx - 300, cy), (cx - 250, cy)], fill=(0, 255, 204, 180), width=2)
    draw.line([(cx + 250, cy), (cx + 300, cy)], fill=(0, 255, 204, 180), width=2)
    draw.line([(cx, cy - 300), (cx, cy - 250)], fill=(0, 255, 204, 180), width=2)
    draw.line([(cx, cy + 250), (cx, cy + 300)], fill=(0, 255, 204, 180), width=2)

    # 3. Outer Hexagonal Metallic Shield Frame
    hex_radius = 140
    angles = np.linspace(0, 2 * np.pi, 7)[:-1] - np.pi / 2
    hex_pts = [(cx + hex_radius * np.cos(a), cy + hex_radius * np.sin(a)) for a in angles]
    
    # Outer Shield Drop Shadow / Base
    draw.polygon(hex_pts, fill=(20, 20, 26, 255), outline=(212, 175, 55, 255), width=4)
    
    # Inner Hex Shield
    inner_hex_pts = [(cx + (hex_radius - 12) * np.cos(a), cy + (hex_radius - 12) * np.sin(a)) for a in angles]
    draw.polygon(inner_hex_pts, fill=(10, 10, 15, 255), outline=(0, 255, 204, 255), width=2)

    # 4. Stylized Interlocking 3D Monogram Crest 'M' & 'D'
    # Left Arm 'M'
    draw.polygon([
        (cx - 70, cy + 60), (cx - 70, cy - 60), (cx - 40, cy - 60),
        (cx - 10, cy + 10), (cx - 10, cy + 60), (cx - 35, cy + 60),
        (cx - 35, cy - 10), (cx - 50, cy + 60)
    ], fill=(212, 175, 55, 255))

    # Right Arm 'M'
    draw.polygon([
        (cx + 70, cy + 60), (cx + 70, cy - 60), (cx + 40, cy - 60),
        (cx + 10, cy + 10), (cx + 10, cy + 60), (cx + 35, cy + 60),
        (cx + 35, cy - 10), (cx + 50, cy + 60)
    ], fill=(255, 215, 0, 255))

    # Center Crown Point
    draw.polygon([
        (cx - 20, cy - 60), (cx, cy - 85), (cx + 20, cy - 60), (cx, cy - 40)
    ], fill=(0, 255, 204, 255))

    # 5. Glowing HUD Text Badge at Bottom
    draw.rounded_rectangle([cx - 150, cy + 220, cx + 150, cy + 255], radius=6, fill=(18, 18, 22, 255), outline=(212, 175, 55, 200), width=1)
    
    # Save image
    img.save(output_path)
    print(f"[OK] Generated 3D Metallic Tech Emblem graphic at '{output_path}' ({width}x{height})")

if __name__ == "__main__":
    generate_tech_emblem_hero()
