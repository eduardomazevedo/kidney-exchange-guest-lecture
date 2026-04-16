from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "kidney_waitlist_flows.csv"
OUTPUT_PATH = ROOT / "images" / "kidney_waitlist_flows.png"


COLORS = {
    "waitlist_deaths": "#C44E52",
    "kidney_exchange": "#55A868",
    "deceased_donor_transplants": "#4C72B0",
    "living_donor_non_exchange": "#8172B3",
    "new_listings": "#222222",
}


LABELS = {
    "waitlist_deaths": "Dying",
    "kidney_exchange": "Kidney exchange",
    "deceased_donor_transplants": "Deceased donor",
    "living_donor_non_exchange": "Other live donor",
    "new_listings": "Joining waitlist",
}


def load_data(path: Path) -> dict[str, list[int]]:
    columns = {
        "year": [],
        "new_listings": [],
        "waitlist_deaths": [],
        "kidney_exchange": [],
        "deceased_donor_transplants": [],
        "living_donor_non_exchange": [],
    }

    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for key in columns:
                columns[key].append(int(row[key]))

    return columns


def main() -> None:
    data = load_data(DATA_PATH)
    years = data["year"]

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(16, 9), constrained_layout=True)

    bar_width = 0.72
    bottom = [0] * len(years)
    stack_order = [
        "deceased_donor_transplants",
        "living_donor_non_exchange",
        "kidney_exchange",
        "waitlist_deaths",
    ]

    for key in stack_order:
        values = data[key]
        ax.bar(
            years,
            values,
            width=bar_width,
            bottom=bottom,
            color=COLORS[key],
            label=LABELS[key],
            edgecolor="white",
            linewidth=0.6,
        )
        bottom = [b + v for b, v in zip(bottom, values)]

    ax.plot(
        years,
        data["new_listings"],
        color=COLORS["new_listings"],
        linewidth=3,
        marker="o",
        markersize=7,
        label=LABELS["new_listings"],
        zorder=5,
    )

    ax.set_title(
        "U.S. kidney waitlist inflow vs exit pathways (2012–2023)",
        fontsize=22,
        pad=18,
    )
    ax.set_xlabel("Year", fontsize=14)
    ax.set_ylabel("People", fontsize=14)
    ax.set_xticks(years)
    ax.set_ylim(0, 50000)
    ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    ax.tick_params(axis="x", rotation=0)
    ax.spines[["top", "right"]].set_visible(False)

    last_x = years[-1]
    ax.annotate(
        f"{LABELS['new_listings']} ({data['new_listings'][-1]:,})",
        xy=(last_x, data["new_listings"][-1]),
        xytext=(18, 10),
        textcoords="offset points",
        color=COLORS["new_listings"],
        fontsize=12,
        fontweight="bold",
        ha="left",
        va="bottom",
    )

    cumulative = [0] * len(years)
    label_x = years[-1] + 0.6
    for key in stack_order:
        values = data[key]
        cumulative = [c + v for c, v in zip(cumulative, values)]
        y = cumulative[-1] - values[-1] / 2
        ax.text(
            years[-1],
            y,
            f"{values[-1]:,}",
            color="black",
            fontsize=11,
            fontweight="bold",
            va="center",
            ha="center",
            zorder=6,
        )
        ax.text(
            label_x,
            y,
            LABELS[key],
            color=COLORS[key],
            fontsize=12,
            fontweight="bold",
            va="center",
            ha="left",
        )

    ax.set_xlim(years[0] - 0.6, years[-1] + 2.2)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved plot to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
