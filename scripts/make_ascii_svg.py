import os
import sys
import base64
from PIL import Image, ImageEnhance, ImageOps

def make_portrait_svg(input_path="prompt2_img.png", output_path="hxni-ascii.svg"):
    """
    Generates a crystal-clear HD animated portrait card SVG.
    Features a clean real photo with an elegant glowing gold laser scanner sweep,
    soft gold ambient trailing aura, cyber corner brackets, and terminal HUD tags.
    """
    print(f"[*] Ingesting portrait photo: {input_path}")
    if not os.path.exists(input_path):
        for fallback in ["prompt2_img.png", "prompt1_img.png", "prompt3_img.png", "hero.png"]:
            if os.path.exists(fallback):
                input_path = fallback
                break

    try:
        img = Image.open(input_path).convert("RGB")
    except Exception as e:
        print(f"[!] Error reading {input_path}: {e}")
        return

    # Enhance contrast and sharpness
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.12)
    
    # Fit photo to canvas aspect ratio (330x390)
    photo_w, photo_h = 330, 390
    img_fitted = ImageOps.fit(img, (photo_w, photo_h), method=Image.Resampling.LANCZOS)
    
    # Base64 encode photo for standalone SVG portability
    import io
    buffer = io.BytesIO()
    img_fitted.save(buffer, format="PNG", quality=95)
    b64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    img_data_uri = f"data:image/png;base64,{b64_str}"

    width = 370
    height = 480
    top_bar_h = 34

    top_photo_y = top_bar_h + 15
    bot_photo_y = top_bar_h + 15 + photo_h

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <style>')
    svg.append('    .term-bg { fill: #0d0d0d; stroke: rgba(212, 175, 55, 0.45); stroke-width: 1.5; rx: 12px; }')
    svg.append('    .top-bar { fill: #161616; rx: 12px; }')
    svg.append('    .dot-red { fill: #FF5F56; }')
    svg.append('    .dot-yellow { fill: #FFBD2E; }')
    svg.append('    .dot-green { fill: #27C93F; }')
    svg.append('    .header-title { font-family: "Fira Code", "Consolas", monospace; font-size: 11px; fill: #888888; font-weight: 600; }')
    svg.append('    .photo-frame { stroke: rgba(212, 175, 55, 0.55); stroke-width: 1.2; rx: 8px; }')
    svg.append('    .hud-text { font-family: "Fira Code", monospace; font-size: 9.5px; fill: #D4AF37; font-weight: 700; letter-spacing: 1px; }')
    svg.append('    .sensor-text { font-family: "Fira Code", monospace; font-size: 8px; fill: #FFD700; font-weight: 700; letter-spacing: 0.5px; }')
    
    # Keyframe Animation for Gold Scanner Sweep
    svg.append('    @keyframes scan-sweep {')
    svg.append(f'      0% {{ transform: translateY({top_photo_y}px); }}')
    svg.append(f'      100% {{ transform: translateY({bot_photo_y}px); }}')
    svg.append('    }')

    svg.append('    .scan-beam-group { animation: scan-sweep 3.6s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite; }')
    svg.append('  </style>')

    # Defs: Soft Gold Ambient Trailing Gradient & ClipPaths
    svg.append('  <defs>')
    # Trailing Soft Gold Aura Gradient
    svg.append('    <linearGradient id="scan-trail-gold" x1="0" y1="1" x2="0" y2="0">')
    svg.append('      <stop offset="0%" stop-color="#FFD700" stop-opacity="0.40" />')
    svg.append('      <stop offset="45%" stop-color="#D4AF37" stop-opacity="0.15" />')
    svg.append('      <stop offset="100%" stop-color="#D4AF37" stop-opacity="0.0" />')
    svg.append('    </linearGradient>')
    
    # Photo ClipPath
    svg.append('    <clipPath id="photo-clip">')
    svg.append(f'      <rect x="20" y="{top_photo_y}" width="{photo_w}" height="{photo_h}" rx="8" />')
    svg.append('    </clipPath>')
    
    svg.append('    <clipPath id="reveal-clip">')
    svg.append(f'      <rect x="0" y="0" width="{width}" height="0">')
    svg.append(f'        <animate attributeName="height" from="0" to="{height}" dur="1.8s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1" />')
    svg.append('      </rect>')
    svg.append('    </clipPath>')
    svg.append('  </defs>')

    # Outer Terminal Frame
    svg.append(f'  <rect x="1" y="1" width="{width-2}" height="{height-2}" class="term-bg" />')

    # Top Bar Header
    svg.append(f'  <path d="M 1 13 C 1 6.36 6.36 1 13 1 L {width-13} 1 C {width-6.36} 1 {width-1} 6.36 {width-1} 13 L {width-1} {top_bar_h} L 1 {top_bar_h} Z" class="top-bar" />')
    svg.append('  <circle cx="18" cy="17" r="5" class="dot-red" />')
    svg.append('  <circle cx="34" cy="17" r="5" class="dot-yellow" />')
    svg.append('  <circle cx="50" cy="17" r="5" class="dot-green" />')
    svg.append(f'  <text x="{width//2}" y="21" text-anchor="middle" class="header-title">DEV-MITUL // PORTRAIT_SCANNER.SYS</text>')
    svg.append(f'  <line x1="1" y1="{top_bar_h}" x2="{width-1}" y2="{top_bar_h}" stroke="rgba(255,255,255,0.08)" stroke-width="1" />')

    # Group wrapped in initial animated reveal
    svg.append('  <g clip-path="url(#reveal-clip)">')
    
    # Layer 1: Base Real High-Res Photo (Clean & Sharp)
    svg.append(f'    <image href="{img_data_uri}" x="20" y="{top_photo_y}" width="{photo_w}" height="{photo_h}" preserveAspectRatio="xMidYMid slice" clip-path="url(#photo-clip)" />')

    # Layer 2: Photo Inner Frame Border
    svg.append(f'    <rect x="20" y="{top_photo_y}" width="{photo_w}" height="{photo_h}" class="photo-frame" fill="none" />')

    # Layer 3: Moving Gold Laser Scanner & Soft Ambient Trailing Aura
    svg.append('    <g clip-path="url(#photo-clip)">')
    svg.append('      <g class="scan-beam-group">')
    # Soft Gold Ambient Trailing Light Aura (45px trailing height)
    svg.append(f'        <rect x="20" y="-45" width="{photo_w}" height="45" fill="url(#scan-trail-gold)" opacity="0.85" />')
    
    # Leading Intense Gold & White Core Laser Line
    svg.append(f'        <line x1="20" y1="0" x2="{20 + photo_w}" y2="0" stroke="#FFD700" stroke-width="3" filter="drop-shadow(0 0 8px #FFD700)" />')
    svg.append(f'        <line x1="20" y1="0" x2="{20 + photo_w}" y2="0" stroke="#FFF8D6" stroke-width="1.2" />')
    
    # HUD Sensor Dots & Status Text
    svg.append('        <circle cx="28" cy="0" r="3.5" fill="#FFD700" />')
    svg.append(f'        <circle cx="{20 + photo_w - 8}" cy="0" r="3.5" fill="#FFD700" />')
    svg.append(f'        <text x="{20 + photo_w - 68}" y="-6" class="sensor-text">[SCAN ACTIVE]</text>')
    svg.append('      </g>')
    svg.append('    </g>')

    # Layer 4: Cyber Corner Brackets
    svg.append(f'    <path d="M 25 {top_photo_y + 15} L 25 {top_photo_y + 5} L 35 {top_photo_y + 5}" stroke="#FFD700" stroke-width="2" fill="none" />')
    svg.append(f'    <path d="M 345 {top_photo_y + 15} L 345 {top_photo_y + 5} L 335 {top_photo_y + 5}" stroke="#FFD700" stroke-width="2" fill="none" />')
    svg.append(f'    <path d="M 25 {bot_photo_y - 15} L 25 {bot_photo_y - 5} L 35 {bot_photo_y - 5}" stroke="#FFD700" stroke-width="2" fill="none" />')
    svg.append(f'    <path d="M 345 {bot_photo_y - 15} L 345 {bot_photo_y - 5} L 335 {bot_photo_y - 5}" stroke="#FFD700" stroke-width="2" fill="none" />')

    # Layer 5: Bottom HUD Overlay Tag Badge
    badge_y = height - 26
    svg.append(f'    <rect x="28" y="{badge_y - 14}" width="314" height="22" fill="rgba(13, 13, 13, 0.88)" stroke="rgba(212, 175, 55, 0.5)" rx="4" />')
    svg.append(f'    <text x="{width//2}" y="{badge_y}" text-anchor="middle" class="hud-text">● DEV-MITUL // AUTOMATION CORE</text>')

    svg.append('  </g>')
    svg.append('</svg>')

    full_svg = "\n".join(svg)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_svg)

    print(f"[OK] Generated Clean Gold Laser Scanner SVG at '{output_path}' ({width}x{height})")

if __name__ == "__main__":
    input_img = sys.argv[1] if len(sys.argv) > 1 else "prompt2_img.png"
    make_portrait_svg(input_img)
