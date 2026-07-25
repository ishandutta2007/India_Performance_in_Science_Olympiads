import argparse
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os

# Data dictionary for all Olympiads
olympiad_data = {
    "IMO": {
        "data": [
            (1989, 25, 50),
            (1990, 17, 54),
            (1991, 10, 56),
            (1992, 21, 56),
            (1993, 15, 73),
            (1994, 16, 69),
            (1995, 24, 73),
            (1996, 14, 75),
            (1997, 21, 82),
            (1998, 7, 76),
            (1999, 18, 81),
            (2000, 14, 82),
            (2001, 7, 83),
            (2002, 9, 84),
            (2003, 15, 82),
            (2004, 14, 85),
            (2005, 36, 91),
            (2006, 35, 90),
            (2007, 25, 93),
            (2008, 31, 97),
            (2009, 28, 104),
            (2010, 36, 95),
            (2011, 23, 101),
            (2012, 11, 100),
            (2013, 29, 97),
            (2014, 39, 101),
            (2015, 37, 104),
            (2016, 34, 109),
            (2017, 52, 111),
            (2018, 28, 107),
            (2019, 15, 112),
            (2021, 26, 107),
            (2022, 24, 104),
            (2023, 9, 112),
            (2024, 4, 108),
            (2025, 7, 115),
            (2026, 7, 117),
        ],
        "top_milestone_threshold": 0.10,
        "peaks": [2024],
        "title_years": "1989-2026",
    },
    "IBO": {
        "data": [
            (2000, 18, 38),
            (2001, 14, 38),
            (2002, 11, 40),
            (2003, 10, 45),
            (2004, 11, 48),
            (2005, 9, 50),
            (2006, 12, 55),
            (2007, 10, 49),
            (2008, 11, 55),
            (2009, 3, 56),
            (2010, 14, 60),
            (2011, 12, 58),
            (2012, 7, 59),
            (2013, 15, 62),
            (2014, 16, 61),
            (2015, 18, 61),
            (2016, 17, 68),
            (2017, 15, 64),
            (2018, 8, 68),
            (2019, 15, 73),
            (2021, 11, 76),
            (2022, 14, 65),
            (2023, 1, 76),
            (2024, 16, 73),
            (2025, 12, 75),
            (2026, 11, 78),
        ],
        "top_milestone_threshold": 0.10,
        "peaks": [2023],
        "title_years": "1989-2026",
    },
    "IChO": {
        "data": [
            (1999, 21, 52),
            (2000, 10, 53),
            (2001, 7, 54),
            (2002, 10, 57),
            (2003, 5, 59),
            (2004, 15, 61),
            (2005, 14, 59),
            (2006, 17, 67),
            (2007, 14, 68),
            (2008, 17, 66),
            (2009, 11, 64),
            (2010, 22, 68),
            (2011, 15, 70),
            (2012, 6, 72),
            (2013, 11, 73),
            (2014, 11, 75),
            (2015, 17, 75),
            (2016, 21, 75),
            (2017, 18, 76),
            (2018, 14, 76),
            (2019, 10, 80),
            (2021, 12, 85),
            (2022, 16, 84),
            (2023, 12, 89),
            (2024, 19, 90),
            (2025, 6, 90),
            (2026, 1, 93),
        ],
        "top_milestone_threshold": 0.10,
        "peaks": [2026],
        "title_years": "1989-2026",
    },
    "IOAA": {
        "data": [
            (2007, 3, 21),
            (2008, 2, 22),
            (2009, 2, 19),
            (2010, 2, 22),
            (2011, 4, 26),
            (2012, 3, 27),
            (2013, 5, 35),
            (2014, 4, 37),
            (2015, 4, 39),
            (2016, 1, 41),
            (2017, 3, 46),
            (2018, 5, 37),
            (2019, 4, 47),
            (2021, 2, 47),
            (2022, 3, 44),
            (2023, 2, 50),
            (2024, 4, 52),
            (2025, 1, 64),
            (2026, 2, 63),
        ],
        "top_milestone_threshold": 0.05,
        "peaks": [2016, 2025],
        "title_years": "1989-2026",
    },
    "IOI": {
        "data": [
            (2002, 33, 77),
            (2003, 35, 75),
            (2004, 30, 81),
            (2005, 34, 72),
            (2006, 27, 74),
            (2007, 31, 76),
            (2008, 33, 78),
            (2009, 36, 78),
            (2010, 32, 80),
            (2011, 33, 78),
            (2012, 38, 81),
            (2013, 29, 77),
            (2014, 25, 81),
            (2015, 27, 83),
            (2016, 26, 80),
            (2017, 30, 83),
            (2018, 28, 87),
            (2019, 31, 87),
            (2020, 24, 87),
            (2021, 26, 88),
            (2022, 23, 89),
            (2023, 19, 87),
            (2024, 18, 91),
            (2025, 15, 90),
            (2026, 12, 92),
        ],
        "top_milestone_threshold": 0.20,
        "peaks": [2026],
        "title_years": "1989-2026",
        "has_2020": True,
    },
    "IPhO": {
        "data": [
            (1998, 15, 56),
            (1999, 20, 62),
            (2000, 14, 63),
            (2001, 11, 65),
            (2002, 8, 66),
            (2003, 7, 54),
            (2004, 16, 71),
            (2005, 11, 73),
            (2006, 14, 86),
            (2007, 10, 69),
            (2008, 6, 82),
            (2009, 4, 68),
            (2010, 9, 79),
            (2011, 6, 84),
            (2012, 16, 81),
            (2013, 8, 83),
            (2014, 8, 85),
            (2015, 11, 82),
            (2016, 8, 84),
            (2017, 5, 88),
            (2018, 1, 86),
            (2019, 7, 78),
            (2021, 5, 76),
            (2022, 6, 75),
            (2023, 5, 80),
            (2024, 4, 43),
            (2025, 5, 87),
            (2026, 1, 87),
        ],
        "top_milestone_threshold": 0.10,
        "peaks": [2018, 2026],
        "title_years": "1998-2026",
    },
}


def plot_olympiad(name):
    if name not in olympiad_data:
        print(
            f"Error: {name} is not a valid Olympiad. Choose from {list(olympiad_data.keys())}"
        )
        sys.exit(1)

    config = olympiad_data[name]
    data = config["data"]

    # Create DataFrame
    df = pd.DataFrame(data, columns=["Year", "Rank", "Total_Countries"])

    # Calculate the competitive percentile (Higher is better, 100% = 1st place)
    df["Percentile"] = (1 - (df["Rank"] - 1) / df["Total_Countries"]) * 100

    # Initialize the plot
    plt.figure(figsize=(18, 10))

    # Plot the primary percentile path
    plt.plot(
        df["Year"],
        df["Percentile"],
        marker="o",
        linestyle="-",
        color="#2c3e50",
        linewidth=2,
        markersize=5,
        alpha=0.8,
        label="India's Performance Percentile",
    )

    # Annotate every individual data point with its Rank / Total Countries string
    prepct = 0
    minpct = 101
    for i, row in df.iterrows():
        year = int(row["Year"])
        rank = int(row["Rank"])
        total = int(row["Total_Countries"])
        pct = row["Percentile"]

        # Toggle text positions slightly to avoid visual overlap
        if pct > prepct:
            yano = 8
        else:
            yano = -14
        xy_text_offset = (0, yano)

        plt.annotate(
            f"{pct:.0f}%ile ({rank}/{total})",
            xy=(year, pct),
            xytext=xy_text_offset,
            textcoords="offset points",
            ha="center",
            fontsize=8,
            color="#34495e",
            weight="semibold",
        )
        prepct = pct
        minpct = min(minpct, pct)

    # Highlight standout historic peaks
    top_milestones = df[
        df["Rank"] / df["Total_Countries"] <= config["top_milestone_threshold"]
    ]
    plt.scatter(
        top_milestones["Year"],
        top_milestones["Percentile"],
        color="#e74c3c",
        s=120,
        zorder=5,
        label="Top 10 Finishes",
    )

    # Specifically label the all-time high water mark(s)
    peaks = config["peaks"]
    if len(peaks) == 1:
        best_year = peaks[0]
        best_data = df[df["Year"] == best_year].iloc[0]
        fmt_pct = (
            f"{best_data['Percentile']:.1f}"
            if name in ["IMO", "IBO", "IOI"]
            else f"{best_data['Percentile']:.0f}"
        )

        # Offset adjustment based on Olympiad to match original visuals
        xytext_offset = 5
        if name == "IMO":
            xytext_offset = 5
        elif name == "IBO":
            xytext_offset = 5
        elif name == "IChO":
            xytext_offset = 5
        elif name == "IOI":
            xytext_offset = 5

        plt.annotate(
            f"🏆 Historic Peak!\nRank {int(best_data['Rank'])} of {int(best_data['Total_Countries'])}\n({fmt_pct}th Percentile)",
            xy=(best_year, best_data["Percentile"]),
            xytext=(
                best_year - xytext_offset,
                best_data["Percentile"] - (6 if name != "IOI" else 2),
            ),
            arrowprops=dict(
                facecolor="#e74c3c", arrowstyle="->", connectionstyle="arc3,rad=-0.1"
            ),
            fontsize=11,
            fontweight="bold",
            color="#e74c3c",
            ha="center",
            fontname="Segoe UI Emoji",
        )
    elif len(peaks) == 2:
        best_1 = df[df["Year"] == peaks[0]].iloc[0]
        best_2 = df[df["Year"] == peaks[1]].iloc[0]

        text_x = 2021 if name == "IOAA" else 2022
        text_y = best_1["Percentile"] + (1 if name == "IOAA" else 2)
        fmt_pct = f"{best_1['Percentile']:.0f}"

        # Main Annotation (Contains the Text + Arrow pointing to first peak)
        plt.annotate(
            f"🏆 Historic Peak!\nRank {int(best_1['Rank'])} of {int(best_1['Total_Countries'])}\n({fmt_pct}th Percentile)",
            xy=(peaks[0], best_1["Percentile"]),
            xytext=(text_x, text_y),
            arrowprops=dict(
                color="#e74c3c", arrowstyle="->", connectionstyle="arc3,rad=-0.1"
            ),
            fontsize=11,
            fontweight="bold",
            color="#e74c3c",
            ha="center",
            fontname="Segoe UI Emoji",
        )
        # Ghost Annotation (Empty Text + Arrow pointing to second peak)
        plt.annotate(
            "",
            xy=(peaks[1], best_2["Percentile"]),
            xytext=(text_x + 1, text_y),
            arrowprops=dict(
                color="#e74c3c",
                arrowstyle="->",
                connectionstyle="arc3,rad=0.1",
            ),
        )

    # Plot customization
    plt.title(
        f"India's {name} Performance Percentile ({config['title_years']})\nRelative Positioning to Overall Pool Size",
        fontsize=16,
        fontweight="bold",
        pad=15,
    )
    plt.xlabel("Year", fontsize=12, labelpad=10)
    plt.ylabel(
        "Competitive Percentile (%) — Higher is Better", fontsize=12, labelpad=10
    )

    plt.xlim(data[0][0] - 1, data[-1][0] + 1)
    plt.ylim(minpct - 6, 103)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="lower left", fontsize=11)

    # Informative visual anchor for the 2020 gap
    if not config.get("has_2020"):
        plt.axvspan(2019.5, 2020.5, color="#ecf0f1", alpha=0.7, zorder=1)
        plt.text(
            2020,
            55,
            "2020\nNo Participation",
            color="#7f8c8d",
            fontsize=9,
            ha="center",
            fontweight="bold",
        )

    plt.tight_layout()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(script_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    plt.savefig(os.path.join(assets_dir, f"india_{name.lower()}_percentile.png"))
    print(f"Generated plot for {name} at assets/india_{name.lower()}_percentile.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Olympiad Performance Plots")
    parser.add_argument(
        "olympiad",
        type=str.upper,
        nargs="?",
        choices=list(olympiad_data.keys()) + ["ALL"],
        default="ALL",
        help="Specify the Olympiad to plot (IMO, IBO, IChO, IOAA, IOI, IPhO, or ALL)",
    )
    args = parser.parse_args()

    if args.olympiad == "ALL":
        for olym in olympiad_data.keys():
            plot_olympiad(olym)
    else:
        plot_olympiad(args.olympiad)
