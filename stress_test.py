import pandas as pd
import matplotlib.pyplot as plt
from city_data import get_canadian_cities
from lbo_engine import simulate_pe_buyout

def run_rate_stress_test():
    df = get_canadian_cities()
    rates = [0.030, 0.040, 0.050, 0.060, 0.070]
    records = []

    for _, row in df.iterrows():
        for r in rates:
            res = simulate_pe_buyout(row, turnover_rate=0.25, reno_cost_per_unit=15000, interest_rate=r)
            records.append({
                "City": row["City"],
                "Rate_%": round(r * 100, 1),
                "IRR_%": res["IRR_%"]
            })

    results_df = pd.DataFrame(records)
    pivot = results_df.pivot(index="City", columns="Rate_%", values="IRR_%")

    print("\n--- PE IRR SENSITIVITY TO MORTGAGE INTEREST RATES ---")
    print(pivot.to_string())

    fig, ax = plt.subplots(figsize=(9, 6))
    for city in pivot.index:
        ax.plot(pivot.columns, pivot.loc[city], marker="o", label=city)

    ax.axhline(15.0, color="black", linestyle="--", label="15% Target IRR")
    ax.set_xlabel("Mortgage Interest Rate (%)")
    ax.set_ylabel("5-Year IRR (%)")
    ax.set_title("Impact of Rising Interest Rates on Canadian PE Buyouts")
    ax.legend()

    plt.tight_layout()
    plt.savefig("charts/rate_sensitivity.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    run_rate_stress_test()
