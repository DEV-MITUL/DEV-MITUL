import os

def make_info_card(output_path="info-card.svg"):
    """
    Generates an ultra-premium, highly detailed, cinematic terminal info card SVG
    titled 'The Cipher Stack' featuring categorized metadata blocks, gold accent badges,
    glowing system status indicators, and sleek typography.
    """
    print("[*] Generating ultra-premium info card SVG...")
    
    width = 490
    height = 480
    top_bar_h = 34
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <style>')
    svg.append('    .card-bg { fill: #0d0d0d; stroke: rgba(212, 175, 55, 0.45); stroke-width: 1.5; rx: 12px; filter: drop-shadow(0 0 12px rgba(212, 175, 55, 0.15)); }')
    svg.append('    .top-bar { fill: #161616; rx: 12px; }')
    svg.append('    .dot-red { fill: #FF5F56; }')
    svg.append('    .dot-yellow { fill: #FFBD2E; }')
    svg.append('    .dot-green { fill: #27C93F; }')
    svg.append('    .header-title { font-family: "Fira Code", "Consolas", monospace; font-size: 11px; fill: #888888; font-weight: 600; }')
    svg.append('    .sec-badge { font-family: "Fira Code", monospace; font-size: 9.5px; fill: #FFD700; font-weight: 700; letter-spacing: 1.5px; }')
    svg.append('    .sec-line { stroke: rgba(212, 175, 55, 0.25); stroke-width: 1; stroke-dasharray: 4,4; }')
    svg.append('    .prompt-symbol { font-family: "Fira Code", monospace; font-size: 11px; fill: #00FFCC; font-weight: bold; }')
    svg.append('    .key-label { font-family: "Fira Code", "Consolas", monospace; font-size: 10.5px; fill: #D4AF37; font-weight: 700; }')
    svg.append('    .val-label { font-family: "Fira Code", "Consolas", monospace; font-size: 10.5px; fill: #E2E2E2; font-weight: 400; }')
    svg.append('    .link-val { fill: #4DA6FF; font-weight: 500; }')
    svg.append('    .status-pill { fill: rgba(39, 201, 63, 0.12); stroke: rgba(39, 201, 63, 0.4); rx: 4px; }')
    svg.append('    .status-text { font-family: "Fira Code", monospace; font-size: 9.5px; fill: #27C93F; font-weight: 700; }')
    svg.append('    .tag-pill { fill: rgba(212, 175, 55, 0.12); stroke: rgba(212, 175, 55, 0.35); rx: 3px; }')
    svg.append('    .tag-text { font-family: "Fira Code", monospace; font-size: 9px; fill: #FFD700; font-weight: 600; }')
    svg.append('    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.2; } }')
    svg.append('    .cursor { fill: #FFD700; animation: blink 1s infinite; }')
    svg.append('  </style>')
    
    # ClipPath reveal for smooth initial loading
    svg.append('  <defs>')
    svg.append('    <clipPath id="card-reveal">')
    svg.append(f'      <rect x="0" y="0" width="{width}" height="0">')
    svg.append(f'        <animate attributeName="height" from="0" to="{height}" dur="1.8s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1" />')
    svg.append('      </rect>')
    svg.append('    </clipPath>')
    svg.append('  </defs>')

    # Outer Frame
    svg.append(f'  <rect x="1" y="1" width="{width-2}" height="{height-2}" class="card-bg" />')
    
    # Header bar
    svg.append(f'  <path d="M 1 13 C 1 6.36 6.36 1 13 1 L {width-13} 1 C {width-6.36} 1 {width-1} 6.36 {width-1} 13 L {width-1} {top_bar_h} L 1 {top_bar_h} Z" class="top-bar" />')
    svg.append('  <circle cx="18" cy="17" r="5" class="dot-red" />')
    svg.append('  <circle cx="34" cy="17" r="5" class="dot-yellow" />')
    svg.append('  <circle cx="50" cy="17" r="5" class="dot-green" />')
    svg.append(f'  <text x="{width//2}" y="21" text-anchor="middle" class="header-title">THE CIPHER STACK // DEV-MITUL v4.2</text>')
    svg.append(f'  <line x1="1" y1="{top_bar_h}" x2="{width-1}" y2="{top_bar_h}" stroke="rgba(255,255,255,0.08)" stroke-width="1" />')

    # Status Pill (Top Right)
    svg.append(f'  <rect x="{width - 128}" y="{top_bar_h + 10}" width="108" height="22" class="status-pill" />')
    svg.append(f'  <text x="{width - 74}" y="{top_bar_h + 24}" text-anchor="middle" class="status-text">● ONLINE // ACTIVE</text>')

    # Content section wrapped in animated clip path
    svg.append('  <g clip-path="url(#card-reveal)">')
    
    y = top_bar_h + 28

    # SECTION 1: SYSTEM & BIOMETRICS
    svg.append(f'    <text x="20" y="{y}" class="sec-badge">SYS METADATA</text>')
    svg.append(f'    <line x1="125" y1="{y-4}" x2="{width-20}" y2="{y-4}" class="sec-line" />')
    
    sys_items = [
        ("Host", "DEV-MITUL Core Engine v4.2"),
        ("OS", "Linux x86_64 (Automation OS)"),
        ("Location", "Bangladesh 🇧🇩")
    ]
    for key, val in sys_items:
        y += 22
        svg.append(f'    <text x="22" y="{y}" class="prompt-symbol">❯</text>')
        svg.append(f'    <text x="36" y="{y}" class="key-label">{key}:</text>')
        svg.append(f'    <text x="110" y="{y}" class="val-label">{val}</text>')

    # SECTION 2: SPECIALIZATION
    y += 28
    svg.append(f'    <text x="20" y="{y}" class="sec-badge">SPECIALIZATION</text>')
    svg.append(f'    <line x1="140" y1="{y-4}" x2="{width-20}" y2="{y-4}" class="sec-line" />')
    
    spec_items = [
        ("Headline", "Automation Expert • Python Expert"),
        ("Role", "Full Stack Engineer • React Architect")
    ]
    for key, val in spec_items:
        y += 22
        svg.append(f'    <text x="22" y="{y}" class="prompt-symbol">❯</text>')
        svg.append(f'    <text x="36" y="{y}" class="key-label">{key}:</text>')
        svg.append(f'    <text x="110" y="{y}" class="val-label">{val}</text>')

    # SECTION 3: TECH ARSENAL MATRIX
    y += 28
    svg.append(f'    <text x="20" y="{y}" class="sec-badge">TECH ARSENAL</text>')
    svg.append(f'    <line x1="125" y1="{y-4}" x2="{width-20}" y2="{y-4}" class="sec-line" />')

    arsenal = [
        ("Frontend", "React, TypeScript, Vite, Tailwind, Three.js"),
        ("Backend", "Node.js, PHP, Python, MySQL, Supabase, Firebase"),
        ("Mobile", "Java, React Native, Flutter"),
        ("Tools", "Git, GitHub, VS Code, Postman, Vercel")
    ]
    for key, val in arsenal:
        y += 22
        svg.append(f'    <text x="22" y="{y}" class="prompt-symbol">❯</text>')
        svg.append(f'    <text x="36" y="{y}" class="key-label">{key}:</text>')
        svg.append(f'    <text x="110" y="{y}" class="val-label">{val}</text>')

    # SECTION 4: DIRECT ENDPOINTS & LINKS
    y += 28
    svg.append(f'    <text x="20" y="{y}" class="sec-badge">ENDPOINTS</text>')
    svg.append(f'    <line x1="105" y1="{y-4}" x2="{width-20}" y2="{y-4}" class="sec-line" />')

    endpoints = [
        ("Portfolio", "https://altalimul.online"),
        ("Topup Web", "https://topupchai.shop"),
        ("Contact", "mitulislam483@gmail.com | Telegram @mitul_islam")
    ]
    for key, val in endpoints:
        y += 22
        svg.append(f'    <text x="22" y="{y}" class="prompt-symbol">❯</text>')
        svg.append(f'    <text x="36" y="{y}" class="key-label">{key}:</text>')
        if "http" in val:
            svg.append(f'    <text x="110" y="{y}" class="val-label link-val">{val}</text>')
        else:
            svg.append(f'    <text x="110" y="{y}" class="val-label">{val}</text>')

    # Terminal Active Cursor Line at bottom
    y += 26
    svg.append(f'    <text x="22" y="{y}" class="prompt-symbol">❯</text>')
    svg.append(f'    <text x="36" y="{y}" class="key-label" fill="#00FFCC">DEV_STATUS:</text>')
    svg.append(f'    <text x="135" y="{y}" class="val-label" fill="#00FFCC">READY FOR DEPLOYMENT</text>')
    svg.append(f'    <rect x="305" y="{y - 10}" width="8" height="12" class="cursor" />')

    svg.append('  </g>')
    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"[OK] Generated ultra-premium info card SVG at '{output_path}' ({width}x{height})")

if __name__ == "__main__":
    make_info_card()
