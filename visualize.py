import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from city_data import get_canadian_cities
from lbo_engine import simulate_pe_buyout

def make_charts():
    df = get_canadian_cities()

    s1 = pd.DataFrame([simulate_pe_buyout(row, 0.10, 0) for _, row in df.iterrows()])
    s2 = pd.DataFrame([simulate_pe_buyout(row, 0.30, 20000) for _, row in df.iterrows()])
    s3 = pd.DataFrame([simulate_pe_buyout(row, 0.30, 20000, force_vacancy_control=True) for _, row in df.iterrows()])

    if not os.path.exists("charts"):
        os.mkdir("charts")

    cities = s1["City"]
    x = np.arange(len(cities))
    w = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))
    b1 = ax.bar(x - w, s1["IRR_%"], w, label="Passive (10% Turnover)")
    b2 = ax.bar(x, s2["IRR_%"], w, label="Value-Add (30% Turnover)")
    b3 = ax.bar(x + w, s3["IRR_%"], w, label="No Vacancy Decontrol")

    ax.axhline(15.0, color="black", linestyle="--", label="15% Target IRR")
    ax.set_ylabel("5-Year IRR (%)")
    ax.set_title("PE Returns by Canadian City & Rent Control Regime")
    ax.set_xticks(x)
    ax.set_xticklabels(cities)
    ax.legend()

    for bars in [b1, b2, b3]:
        for bar in bars:
            h = bar.get_height()
            if not np.isnan(h):
                ax.text(bar.get_x() + bar.get_width() / 2, h + 0.3, f"{h:.1f}%", ha="center", fontsize=8)

    plt.tight_layout()
    plt.savefig("charts/irr_comparison.png", dpi=300)

    fig2, ax2 = plt.subplots(figsize=(9, 6))
    ax2.scatter(s2["5Yr_Rent_Hike_%"], s2["IRR_%"], s=120, label="Current Rules")
    ax2.scatter(s3["5Yr_Rent_Hike_%"], s3["IRR_%"], s=120, marker="s", label="Strict Rent Control")

    for i in range(len(cities)):
        ax2.text(s2["5Yr_Rent_Hike_%"][i] + 0.5, s2["IRR_%"][i] + 0.2, cities[i], fontsize=9)
        ax2.annotate("", xy=(s3["5Yr_Rent_Hike_%"][i], s3["IRR_%"][i]),
                     xytext=(s2["5Yr_Rent_Hike_%"][i], s2["IRR_%"][i]),
                     arrowprops=dict(arrowstyle="->", color="gray"))

    ax2.axhline(15.0, color="black", linestyle="--", label="15% Target IRR")
    ax2.set_xlabel("5-Year Rent Increase (%)")
    ax2.set_ylabel("PE Fund IRR (%)")
    ax2.set_title("Tenant Rent Hikes vs. Fund IRR")
    ax2.legend()

    plt.tight_layout()
    plt.savefig("charts/rent_vs_irr.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    make_charts()
