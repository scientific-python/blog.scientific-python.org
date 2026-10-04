"""A teaching example; it is not dataHabibi's production implementation.

SPDX-License-Identifier: BSD-3-Clause
Copyright (c) 2026 dataHabibi
"""

import csv
import io
from pathlib import Path
from urllib.request import urlopen

import matplotlib.pyplot as plt


DATA_URL = (
    "https://huggingface.co/datasets/datahabibi/"
    "dubai-community-rental-yields-2026-06/resolve/"
    "91060eb7aa665201a2950916122a44008a048e31/"
    "dubai-community-yields-2026-06.csv"
)


def load_snapshot():
    """Read the pinned public snapshot without changing its missing values."""
    with urlopen(DATA_URL, timeout=30) as response:
        text = response.read().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    required = {
        "community",
        "gross_yield_pct",
        "buildings_tracked",
        "yield_sample_size",
    }
    if not required.issubset(reader.fieldnames or []):
        raise ValueError("The CSV is missing a required column")

    rows = []
    for raw in reader:
        sample = raw["yield_sample_size"].strip()
        rows.append(
            {
                "community": raw["community"],
                "yield": float(raw["gross_yield_pct"]),
                "tracked": int(raw["buildings_tracked"]),
                "sample": int(sample) if sample else None,
            }
        )
    return rows


def plot_context(rows):
    """Keep the city reference separate and align two panels by community."""
    city_rows = [row for row in rows if row["community"] == "Dubai city average"]
    if len(city_rows) != 1:
        raise ValueError("Expected one separately reported city reference")
    city = city_rows[0]
    communities = [row for row in rows if row["community"] != city["community"]]
    communities.sort(key=lambda row: (-row["yield"], row["community"]))
    positions = list(range(len(communities)))

    with plt.rc_context({"font.size": 10, "axes.titleweight": "bold"}):
        fig, (yield_ax, count_ax) = plt.subplots(
            1,
            2,
            figsize=(14, 8.4),
            sharey=True,
            layout="constrained",
            gridspec_kw={"width_ratios": [1.2, 1]},
        )
        bars = yield_ax.barh(
            positions,
            [row["yield"] for row in communities],
            color="#286b91",
            height=0.58,
        )
        yield_ax.bar_label(bars, fmt="%.2f%%", padding=4, fontsize=9)
        yield_ax.set_yticks(positions, labels=[row["community"] for row in communities])
        yield_ax.invert_yaxis()
        yield_ax.set_xlim(0, 11)
        yield_ax.set_title("Gross rental yield", loc="left", pad=40)
        yield_ax.set_xlabel("Percent, as reported in the snapshot")
        yield_ax.axvline(
            city["yield"],
            color="#515b63",
            linestyle="--",
            linewidth=1.2,
            label=f"Reported city reference: {city['yield']:.2f}%",
        )
        yield_ax.legend(loc="lower left", frameon=False, fontsize=9)

        count_ax.scatter(
            [row["tracked"] for row in communities],
            positions,
            facecolors="white",
            edgecolors="#8f4b2f",
            linewidths=1.5,
            s=52,
            label="Buildings tracked",
            zorder=3,
        )
        known = [
            (pos, row)
            for pos, row in zip(positions, communities)
            if row["sample"] is not None
        ]
        count_ax.scatter(
            [row["sample"] for _, row in known],
            [pos for pos, _ in known],
            color="#6554a4",
            marker="s",
            s=24,
            label="Yield sample (buildings)",
            zorder=4,
        )
        for pos, row in zip(positions, communities):
            sample_text = "missing" if row["sample"] is None else str(row["sample"])
            count_ax.annotate(
                f"{sample_text} / {row['tracked']}",
                (max(row["sample"] or 0, row["tracked"]) + 8, pos),
                va="center",
                fontsize=8,
            )
        count_ax.set_xlim(0, max(row["tracked"] for row in communities) * 1.28)
        count_ax.set_title("Two different coverage counts", loc="left", pad=40)
        count_ax.set_xlabel("Buildings; labels show sample / tracked")
        count_ax.legend(
            loc="lower left", bbox_to_anchor=(0, 1.01), frameon=False, fontsize=9
        )

        for ax in (yield_ax, count_ax):
            ax.set_axisbelow(True)
            ax.grid(axis="x", color="#e3e7ea", linewidth=0.8)
            ax.spines[["top", "right", "left"]].set_visible(False)
            ax.tick_params(axis="y", length=0)

        city_sample = "missing" if city["sample"] is None else str(city["sample"])
        fig.suptitle(
            "June 2026 Dubai community snapshot\n"
            f"City row: {city['tracked']:,} buildings tracked; "
            f"yield sample size {city_sample}. Counts are not confidence intervals.",
            fontsize=13,
        )
        return fig


if __name__ == "__main__":
    rows = load_snapshot()
    fig = plot_context(rows)
    output = Path(__file__).with_name("coverage-context.png")
    fig.savefig(output, dpi=160, facecolor="white", pil_kwargs={"optimize": True})
    plt.close(fig)
    print(f"Rendered {len(rows)} source rows to {output.name}")
