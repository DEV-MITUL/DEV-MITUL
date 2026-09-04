import os
import json
import datetime

# Dark / Gold / Emerald palette mapping for 5 activity levels
COLOR_MAP = {
    0: "#161616",  # Empty / No activity
    1: "#3b3012",  # Low activity
    2: "#785f18",  # Medium activity
    3: "#b8901e",  # High activity
    4: "#ffd700"   # Extreme activity (Gold highlight)
}

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
WEEKDAY_NAMES = ["Mon", "Wed", "Fri"]

def render_heatmap_svg(json_path="data/contributions.json", output_path="contrib-heatmap.svg"):
    print(f"[*] Reading contribution data from '{json_path}'...")
    if not os.path.exists(json_path):
        print(f"[!] File '{json_path}' not found. Run fetch_contributions.py first.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_contributions = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)
    best_day = data.get("best_day", {"date": "N/A", "count": 0})
    days = data.get("days", [])

    # Layout SVG Dimensions
    width = 860
    height = 240
    top_bar_h = 75
    cell_size = 11.5
    cell_gap = 3.5
    grid_start_x = 45
    grid_start_y = top_bar_h + 30

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <style>')
    svg.append('    .heatmap-bg { fill: #0d0d0d; stroke: rgba(212, 175, 55, 0.4); stroke-width: 1.5; rx: 12px; }')
    svg.append('    .metric-card { fill: #161616; stroke: rgba(212, 175, 55, 0.25); stroke-width: 1; rx: 8px; }')
    svg.append('    .metric-val { font-family: "Fira Code", "Consolas", monospace; font-size: 15px; fill: #FFD700; font-weight: 700; }')
    svg.append('    .metric-lbl { font-family: "Fira Code", "Consolas", monospace; font-size: 9.5px; fill: #888888; text-transform: uppercase; font-weight: 600; }')
    svg.append('    .axis-label { font-family: "Fira Code", "Consolas", monospace; font-size: 9px; fill: #777777; }')
    svg.append('    .day-cell { rx: 2.5px; transition: all 0.2s ease; }')
    svg.append('    .day-cell:hover { stroke: #FFD700; stroke-width: 1.5px; }')
    svg.append('    .legend-text { font-family: "Fira Code", monospace; font-size: 9px; fill: #777777; }')
    svg.append('  </style>')

    # Background rect
    svg.append(f'  <rect x="1" y="1" width="{width-2}" height="{height-2}" class="heatmap-bg" />')

    # Metric Cards across Top Bar
    metrics = [
        ("CONTRIBUTIONS", f"{total_contributions:,}"),
        ("CURRENT STREAK", f"{current_streak} days"),
        ("LONGEST STREAK", f"{longest_streak} days"),
        ("BEST DAY", f"{best_day['count']} ({best_day['date']})")
    ]

    card_w = (width - 40 - (3 * 12)) // 4
    card_h = 46
    for i, (label, val) in enumerate(metrics):
        cx = 20 + i * (card_w + 12)
        cy = 16
        svg.append(f'  <rect x="{cx}" y="{cy}" width="{card_w}" height="{card_h}" class="metric-card" />')
        svg.append(f'  <text x="{cx + 12}" y="{cy + 18}" class="metric-lbl">{label}</text>')
        svg.append(f'  <text x="{cx + 12}" y="{cy + 37}" class="metric-val">{val}</text>')

    # Group days into weeks (columns of 7 days, Sunday=0 to Saturday=6)
    weeks = []
    current_week = []
    
    # Track month labels position
    month_positions = []
    last_month = None

    for item in days:
        dt = datetime.datetime.strptime(item["date"], "%Y-%m-%d")
        w_day = (dt.weekday() + 1) % 7 # 0=Sunday, 1=Monday... 6=Saturday
        
        # Check for month label change
        month_str = MONTH_NAMES[dt.month - 1]
        if month_str != last_month:
            last_month = month_str
            # We record week index for this month tag
            month_positions.append((len(weeks), month_str))

        if w_day == 0 and current_week:
            weeks.append(current_week)
            current_week = []
            
        current_week.append(item)

    if current_week:
        weeks.append(current_week)

    # Render Month Labels
    for week_idx, month_name in month_positions:
        mx = grid_start_x + week_idx * (cell_size + cell_gap)
        svg.append(f'  <text x="{mx:.1f}" y="{grid_start_y - 8}" class="axis-label">{month_name}</text>')

    # Render Weekday Labels (Mon, Wed, Fri)
    weekday_y_offsets = [
        (1, "Mon", grid_start_y + 1 * (cell_size + cell_gap) + 9),
        (3, "Wed", grid_start_y + 3 * (cell_size + cell_gap) + 9),
        (5, "Fri", grid_start_y + 5 * (cell_size + cell_gap) + 9),
    ]
    for _, name, wy in weekday_y_offsets:
        svg.append(f'  <text x="18" y="{wy:.1f}" class="axis-label">{name}</text>')

    # Render Grid Cells
    for w_idx, week in enumerate(weeks):
        x_pos = grid_start_x + w_idx * (cell_size + cell_gap)
        for d_idx, day_info in enumerate(week):
            # Day index 0..6
            dt = datetime.datetime.strptime(day_info["date"], "%Y-%m-%d")
            row_idx = (dt.weekday() + 1) % 7
            y_pos = grid_start_y + row_idx * (cell_size + cell_gap)
            
            level = day_info.get("level", 0)
            fill_color = COLOR_MAP.get(level, COLOR_MAP[0])
            count = day_info.get("count", 0)
            date_str = day_info.get("date", "")
            
            svg.append(f'  <rect x="{x_pos:.1f}" y="{y_pos:.1f}" width="{cell_size}" height="{cell_size}" fill="{fill_color}" class="day-cell">')
            svg.append(f'    <title>{count} contributions on {date_str}</title>')
            svg.append('  </rect>')

    # Bottom Legend: Less [ 0 1 2 3 4 ] More
    legend_x = width - 180
    legend_y = height - 16
    svg.append(f'  <text x="{legend_x - 30}" y="{legend_y + 9}" class="legend-text">Less</text>')
    for l in range(5):
        lx = legend_x + l * (cell_size + 4)
        svg.append(f'  <rect x="{lx}" y="{legend_y}" width="{cell_size}" height="{cell_size}" fill="{COLOR_MAP[l]}" class="day-cell" />')
    svg.append(f'  <text x="{legend_x + 5 * (cell_size + 4) + 6}" y="{legend_y + 9}" class="legend-text">More</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"[OK] Rendered contribution heatmap SVG at '{output_path}' ({width}x{height})")

if __name__ == "__main__":
    render_heatmap_svg()
