import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

# Set high DPI and aesthetic defaults for Matplotlib
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 1.2

from plot_olympiad import olympiad_data

OLYMPIAD_META = {
    "IMO": {
        "full_name": "International Mathematical Olympiad",
        "color": "#2563eb",       # Royal Blue
        "light_color": "#eff6ff",
        "icon_label": "MATHEMATICS",
    },
    "IPhO": {
        "full_name": "International Physics Olympiad",
        "color": "#7c3aed",      # Deep Purple
        "light_color": "#f5f3ff",
        "icon_label": "PHYSICS",
    },
    "IChO": {
        "full_name": "International Chemistry Olympiad",
        "color": "#059669",      # Emerald Green
        "light_color": "#ecfdf5",
        "icon_label": "CHEMISTRY",
    },
    "IBO": {
        "full_name": "International Biology Olympiad",
        "color": "#db2777",      # Pink / Rose
        "light_color": "#fdf2f8",
        "icon_label": "BIOLOGY",
    },
    "IOI": {
        "full_name": "International Olympiad in Informatics",
        "color": "#ea580c",      # Vivid Orange
        "light_color": "#fff7ed",
        "icon_label": "INFORMATICS",
    },
    "IOAA": {
        "full_name": "International Olympiad on Astronomy & Astrophysics",
        "color": "#0284c7",      # Sky Blue
        "light_color": "#f0f9ff",
        "icon_label": "ASTRONOMY",
    },
}

WIDTH = 1280
HEIGHT = 640
DPI = 100

def fig_to_pil(fig):
    """Converts a Matplotlib figure to a PIL RGB Image with exact canvas size."""
    fig.canvas.draw()
    rgba = np.asarray(fig.canvas.buffer_rgba())
    img = Image.fromarray(rgba).convert('RGB')
    plt.close(fig)
    return img

def create_hero_slide():
    """Generates a sleek, high-impact cover/hero slide for social preview."""
    img = Image.new('RGB', (WIDTH, HEIGHT), color='#0f172a')
    draw = ImageDraw.Draw(img)

    # Background grid lines
    for x in range(0, WIDTH, 40):
        draw.line([(x, 0), (x, HEIGHT)], fill='#1e293b', width=1)
    for y in range(0, HEIGHT, 40):
        draw.line([(0, y), (WIDTH, y)], fill='#1e293b', width=1)

    # Top accent bar (Tricolor subtle hint)
    draw.rectangle([(0, 0), (WIDTH // 3, 6)], fill='#f97316')
    draw.rectangle([(WIDTH // 3, 0), (2 * WIDTH // 3, 6)], fill='#f8fafc')
    draw.rectangle([(2 * WIDTH // 3, 0), (WIDTH, 6)], fill='#22c55e')

    def load_font(font_name, size):
        size = int(size)
        for p in [f"C:/Windows/Fonts/{font_name}", "C:/Windows/Fonts/arial.ttf", font_name]:
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
        return ImageFont.load_default()

    font_title = load_font("segoeuib.ttf", 40)
    font_sub = load_font("segoeui.ttf", 20)
    font_card_title = load_font("segoeuib.ttf", 17)
    font_card_sub = load_font("segoeui.ttf", 13)
    font_card_stat = load_font("segoeuib.ttf", 14)
    font_footer = load_font("segoeui.ttf", 14)

    # Header text
    draw.text((WIDTH // 2, 45), "INDIA IN INTERNATIONAL SCIENCE OLYMPIADS", fill='#f8fafc', font=font_title, anchor='mm')
    draw.text((WIDTH // 2, 85), "Historical Performance, Percentile Rankings & Global Excellence (1989 - 2026)", fill='#94a3b8', font=font_sub, anchor='mm')

    # Grid layout for 6 cards
    card_w, card_h = 360, 190
    coords = [
        (80, 130),   (460, 130),   (840, 130),
        (80, 350),   (460, 350),   (840, 350),
    ]

    keys = ["IMO", "IPhO", "IChO", "IBO", "IOI", "IOAA"]
    
    for idx, key in enumerate(keys):
        cx, cy = coords[idx]
        meta = OLYMPIAD_META[key]
        cfg = olympiad_data[key]
        df = pd.DataFrame(cfg["data"], columns=["Year", "Rank", "Total_Countries"])
        df["Percentile"] = (1 - (df["Rank"] - 1) / df["Total_Countries"]) * 100

        best_row = df.loc[df["Percentile"].idxmax()]
        best_rank = int(best_row["Rank"])
        best_total = int(best_row["Total_Countries"])
        best_year = int(best_row["Year"])
        best_pct = best_row["Percentile"]

        start_yr = int(df["Year"].min())
        end_yr = int(df["Year"].max())

        # Card container background & border
        draw.rounded_rectangle([(cx, cy), (cx + card_w, cy + card_h)], radius=12, fill='#1e293b', outline=meta["color"], width=2)
        
        # Badge
        draw.rounded_rectangle([(cx + 15, cy + 15), (cx + 105, cy + 42)], radius=6, fill=meta["color"])
        draw.text((cx + 60, cy + 28), key, fill='#ffffff', font=font_card_title, anchor='mm')

        # Full name & subject
        draw.text((cx + 120, cy + 28), meta["icon_label"], fill='#cbd5e1', font=font_card_sub, anchor='lm')

        # Stat 1: Best Rank / Peak
        peak_str = f"Historic Peak: Rank {best_rank} of {best_total} ({best_year})"
        draw.text((cx + 18, cy + 68), peak_str, fill='#38bdf8' if best_rank <= 5 else '#f8fafc', font=font_card_stat)

        # Stat 2: Percentile
        pct_str = f"Top Percentile: {best_pct:.1f}%ile"
        draw.text((cx + 18, cy + 96), pct_str, fill='#4ade80', font=font_card_sub)

        # Stat 3: Latest 2026 Rank
        last_row = df.iloc[-1]
        last_rank = int(last_row["Rank"])
        last_total = int(last_row["Total_Countries"])
        last_str = f"Latest (2026): Rank {last_rank} of {last_total}"
        draw.text((cx + 18, cy + 122), last_str, fill='#94a3b8', font=font_card_sub)

        # Stat 4: Years range
        draw.text((cx + 18, cy + 148), f"Participating Years: {len(df)}  |  {start_yr} - {end_yr}", fill='#64748b', font=font_card_sub)

    # Footer banner
    draw.rectangle([(0, 585), (WIDTH, HEIGHT)], fill='#0b132b')
    draw.text((WIDTH // 2, 612), "30+ Years of Data  |  Multi-Disciplinary Analysis  |  Interactive Visualizations", fill='#94a3b8', font=font_footer, anchor='mm')

    return img

def create_olympiad_slide(name):
    """Generates a standalone plot frame for a specific Olympiad with clean formatting."""
    config = olympiad_data[name]
    meta = OLYMPIAD_META[name]
    data = config["data"]

    df = pd.DataFrame(data, columns=["Year", "Rank", "Total_Countries"])
    df["Percentile"] = (1 - (df["Rank"] - 1) / df["Total_Countries"]) * 100

    fig, ax = plt.subplots(figsize=(WIDTH / DPI, HEIGHT / DPI), dpi=DPI)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#f8fafc')

    # Main percentile plot line
    ax.plot(
        df["Year"],
        df["Percentile"],
        marker="o",
        linestyle="-",
        color=meta["color"],
        linewidth=2.5,
        markersize=5.5,
        alpha=0.9,
        label="India's Performance Percentile",
        zorder=3,
    )

    # Annotate points cleanly without collisions
    prepct = 0
    minpct = 101
    n_pts = len(df)
    for i, row in df.iterrows():
        year = int(row["Year"])
        rank = int(row["Rank"])
        total = int(row["Total_Countries"])
        pct = row["Percentile"]

        # Smart alternating offsets for clean text placement
        if pct >= prepct:
            yano = 9 if (i % 2 == 0) else 14
        else:
            yano = -15 if (i % 2 == 0) else -20

        ax.annotate(
            f"{pct:.0f}%ile ({rank}/{total})",
            xy=(year, pct),
            xytext=(0, yano),
            textcoords="offset points",
            ha="center",
            fontsize=7.2,
            color="#334155",
            weight="semibold",
            zorder=4,
        )
        prepct = pct
        minpct = min(minpct, pct)

    # Highlight top milestones
    top_milestones = df[df["Rank"] / df["Total_Countries"] <= config["top_milestone_threshold"]]
    ax.scatter(
        top_milestones["Year"],
        top_milestones["Percentile"],
        color="#ef4444",
        s=95,
        zorder=5,
        label=f"Top {int(config['top_milestone_threshold']*100)}% Finishes",
        edgecolors='#ffffff',
        linewidth=1.4,
    )

    # Custom positioning for peak boxes to prevent overlap
    peaks = config["peaks"]
    if len(peaks) == 1:
        best_year = peaks[0]
        best_data = df[df["Year"] == best_year].iloc[0]
        fmt_pct = f"{best_data['Percentile']:.1f}" if name in ["IMO", "IBO", "IOI"] else f"{best_data['Percentile']:.0f}"

        # Position offsets specific to each Olympiad shape
        if name == "IMO":
            xytext_pos = (2018, 96)
        elif name == "IBO":
            xytext_pos = (2016, 95)
        elif name == "IChO":
            xytext_pos = (2020, 94)
        elif name == "IOI":
            xytext_pos = (2020, 78)
        else:
            xytext_pos = (best_year - 4, best_data["Percentile"] - 8)

        ax.annotate(
            f"Historic Peak!\nRank {int(best_data['Rank'])} of {int(best_data['Total_Countries'])}\n({fmt_pct}th Percentile)",
            xy=(best_year, best_data["Percentile"]),
            xytext=xytext_pos,
            arrowprops=dict(
                facecolor="#ef4444", edgecolor="#ef4444", arrowstyle="->", lw=1.8, connectionstyle="arc3,rad=-0.1"
            ),
            fontsize=9.5,
            fontweight="bold",
            color="#dc2626",
            ha="center",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#fee2e2", edgecolor="#ef4444", lw=1),
            zorder=6,
        )
    elif len(peaks) == 2:
        best_1 = df[df["Year"] == peaks[0]].iloc[0]
        best_2 = df[df["Year"] == peaks[1]].iloc[0]

        if name == "IPhO":
            text_x, text_y = 2022, 92
        elif name == "IOAA":
            text_x, text_y = 2020, 91
        else:
            text_x, text_y = 2021, best_1["Percentile"] - 7

        fmt_pct = f"{best_1['Percentile']:.0f}"

        ax.annotate(
            f"Historic Peak!\nRank {int(best_1['Rank'])} of {int(best_1['Total_Countries'])}\n({fmt_pct}th Percentile)",
            xy=(peaks[0], best_1["Percentile"]),
            xytext=(text_x, text_y),
            arrowprops=dict(
                edgecolor="#ef4444", facecolor="#ef4444", arrowstyle="->", lw=1.8, connectionstyle="arc3,rad=-0.1"
            ),
            fontsize=9.5,
            fontweight="bold",
            color="#dc2626",
            ha="center",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#fee2e2", edgecolor="#ef4444", lw=1),
            zorder=6,
        )
        ax.annotate(
            "",
            xy=(peaks[1], best_2["Percentile"]),
            xytext=(text_x + 0.5, text_y + 1),
            arrowprops=dict(
                edgecolor="#ef4444", facecolor="#ef4444", arrowstyle="->", lw=1.8, connectionstyle="arc3,rad=0.1"
            ),
            zorder=6,
        )

    # 2020 Pandemic gap styling
    if not config.get("has_2020"):
        ax.axvspan(2019.5, 2020.5, color="#e2e8f0", alpha=0.7, zorder=1)
        ax.text(
            2020,
            max(45, minpct - 3),
            "2020\nNo Event",
            color="#64748b",
            fontsize=8.5,
            ha="center",
            fontweight="bold",
        )

    start_yr = int(df["Year"].min())
    end_yr = int(df["Year"].max())

    # Title & Formatting
    ax.set_title(
        f"India's {name} ({meta['full_name']}) Performance Percentile ({start_yr}–{end_yr})",
        fontsize=14,
        fontweight="bold",
        color="#0f172a",
        pad=12,
    )
    ax.set_xlabel("Year", fontsize=11, color="#334155", labelpad=8)
    ax.set_ylabel("Competitive Percentile (%) — Higher is Better", fontsize=11, color="#334155", labelpad=8)

    ax.set_xlim(df["Year"].min() - 1, df["Year"].max() + 1)
    ax.set_ylim(max(40, minpct - 8), 104)
    ax.grid(True, linestyle=":", alpha=0.6, color="#cbd5e1")
    ax.legend(loc="lower left", fontsize=9.5, framealpha=0.9, facecolor='#ffffff')

    # Summary overlay badge on plot
    latest_row = df.iloc[-1]
    info_box_text = f"Latest Result (2026): Rank {int(latest_row['Rank'])} / {int(latest_row['Total_Countries'])} ({latest_row['Percentile']:.1f}%ile)"
    ax.text(
        0.98, 0.04,
        info_box_text,
        transform=ax.transAxes,
        fontsize=9.5,
        fontweight='bold',
        color='#0f172a',
        ha='right',
        va='bottom',
        bbox=dict(boxstyle="round,pad=0.5", facecolor=meta["light_color"], edgecolor=meta["color"], lw=1.5)
    )

    plt.tight_layout()
    return fig_to_pil(fig)

def create_overview_slide():
    """Generates a master comparative slide overlaying all 6 Olympiads on one chart."""
    fig, ax = plt.subplots(figsize=(WIDTH / DPI, HEIGHT / DPI), dpi=DPI)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#f8fafc')

    for key, meta in OLYMPIAD_META.items():
        cfg = olympiad_data[key]
        df = pd.DataFrame(cfg["data"], columns=["Year", "Rank", "Total_Countries"])
        df["Percentile"] = (1 - (df["Rank"] - 1) / df["Total_Countries"]) * 100
        
        ax.plot(
            df["Year"],
            df["Percentile"],
            marker="o",
            linestyle="-",
            color=meta["color"],
            linewidth=2.3,
            markersize=4.5,
            alpha=0.85,
            label=f"{key} ({meta['icon_label']})"
        )

    ax.set_title(
        "India across All 6 International Science Olympiads (Comparative Percentile Overview)",
        fontsize=14.5,
        fontweight="bold",
        color="#0f172a",
        pad=12,
    )
    ax.set_xlabel("Year", fontsize=11, color="#334155", labelpad=8)
    ax.set_ylabel("Competitive Percentile (%)", fontsize=11, color="#334155", labelpad=8)

    ax.set_xlim(1988, 2027)
    ax.set_ylim(48, 103)
    ax.grid(True, linestyle=":", alpha=0.6, color="#cbd5e1")
    ax.legend(loc="lower left", fontsize=9.5, ncol=3, framealpha=0.95, facecolor='#ffffff', edgecolor='#cbd5e1')

    # Highlight 90th percentile threshold
    ax.axhline(90, color="#ef4444", linestyle="--", alpha=0.5, linewidth=1.5)
    ax.text(1989, 90.8, "90th Percentile Benchmark (Top 10% Globally)", color="#dc2626", fontsize=9, fontweight="bold")

    plt.tight_layout()
    return fig_to_pil(fig)

def build_social_preview_gif():
    """Compiles all slides and transition frames into a robust, high-quality GIF."""
    print("Generating refined slides...")
    
    # Generate main slides
    slide_hero = create_hero_slide()
    slides = [slide_hero]
    
    olympiad_keys = ["IMO", "IPhO", "IChO", "IBO", "IOI", "IOAA"]
    for key in olympiad_keys:
        print(f"  Rendering {key} slide...")
        slides.append(create_olympiad_slide(key))

    print("  Rendering Master Overview slide...")
    slides.append(create_overview_slide())

    # Build sequence of frames with smooth cross-fade transitions
    frames = []
    durations = []

    HERO_DURATION = 3000       # 3.0s for cover slide
    PLOT_DURATION = 2500       # 2.5s for each chart slide
    OVERVIEW_DURATION = 3200   # 3.2s for final overview dashboard slide
    TRANSITION_STEPS = 0       # Clean direct slide cut for maximum crispness and optimal GIF compression
    TRANSITION_DUR = 0

    n_slides = len(slides)
    for i in range(n_slides):
        current_slide = slides[i]
        next_slide = slides[(i + 1) % n_slides]

        # Add main slide frame
        frames.append(current_slide)
        if i == 0:
            durations.append(HERO_DURATION)
        elif i == n_slides - 1:
            durations.append(OVERVIEW_DURATION)
        else:
            durations.append(PLOT_DURATION)

        # Add transition frames if specified
        for step in range(1, TRANSITION_STEPS + 1):
            alpha = step / (TRANSITION_STEPS + 1)
            blended = Image.blend(current_slide, next_slide, alpha)
            frames.append(blended)
            durations.append(TRANSITION_DUR)

    print("Quantizing and compiling GIF...")
    # Quantize frames to 256-color palette with no dithering for crisp text/lines and high LZW compression ratio
    quantized_frames = [
        frame.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        for frame in frames
    ]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(script_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    target_hyphen = os.path.join(assets_dir, "social-preview.gif")
    target_underscore = os.path.join(assets_dir, "social_preview.gif")

    # Save to assets/social-preview.gif
    quantized_frames[0].save(
        target_hyphen,
        save_all=True,
        append_images=quantized_frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
        optimize=True,
    )
    print(f"Generated {target_hyphen} (Size: {os.path.getsize(target_hyphen) / 1024:.1f} KB)")

    # Save copy to assets/social_preview.gif
    quantized_frames[0].save(
        target_underscore,
        save_all=True,
        append_images=quantized_frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
        optimize=True,
    )
    print(f"Generated {target_underscore} (Size: {os.path.getsize(target_underscore) / 1024:.1f} KB)")

if __name__ == "__main__":
    build_social_preview_gif()
