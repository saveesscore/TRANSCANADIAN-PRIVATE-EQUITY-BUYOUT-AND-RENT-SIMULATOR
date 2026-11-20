import pandas as pd
import matplotlib.pyplot as plt
from city_data import get_canadian_cities

def simulate_buy_vs_rent(city_row, years=10, mortgage_rate=0.045, down_payment_pct=0.20,
                         home_appreciation=0.03, stock_return=0.075, prop_tax_rate=0.01):
    home_price = city_row["Price_Per_Unit"]
    monthly_rent = city_row["Market_Rent"]
    rent_cap = min(city_row["Rent_Cap"], 0.035)

    down_payment = home_price * down_payment_pct
    loan = home_price - down_payment
    monthly_rate = mortgage_rate / 12
    n_payments = 25 * 12

    if monthly_rate > 0:
        monthly_mortgage = loan * (monthly_rate * (1 + monthly_rate)**n_payments) / ((1 + monthly_rate)**n_payments - 1)
    else:
        monthly_mortgage = loan / n_payments

    balance = loan
    current_home_val = home_price
    current_rent = monthly_rent
    stock_portfolio = down_payment

    for year in range(1, years + 1):
        for month in range(12):
            interest = balance * monthly_rate
            principal = monthly_mortgage - interest
            balance = max(0, balance - principal)

            monthly_owner_cost = monthly_mortgage + (current_home_val * prop_tax_rate / 12) + (current_home_val * 0.01 / 12) + 450
            monthly_savings = monthly_owner_cost - current_rent

            stock_portfolio = (stock_portfolio + monthly_savings) * (1 + stock_return / 12)

        current_home_val *= (1 + home_appreciation)
        current_rent *= (1 + rent_cap)

    selling_costs = current_home_val * 0.05
    buyer_net_worth = current_home_val - balance - selling_costs
    renter_net_worth = stock_portfolio

    return {
        "City": city_row["City"],
        "Buyer_Net_Worth": round(buyer_net_worth, 0),
        "Renter_Net_Worth": round(renter_net_worth, 0),
        "Advantage": "Buy" if buyer_net_worth > renter_net_worth else "Rent + Invest",
        "Diff": round(buyer_net_worth - renter_net_worth, 0)
    }

def run_buy_vs_rent_stress_test():
    df = get_canadian_cities()

    print("\n=== 10-YEAR BUY VS. RENT + INVEST (4.5% Mortgage Rate, 7.5% Stock Return) ===")
    base = pd.DataFrame([simulate_buy_vs_rent(r, years=10, mortgage_rate=0.045) for _, r in df.iterrows()])
    print(base.to_string(index=False))

    rates = [0.025, 0.035, 0.045, 0.055, 0.065]
    stress_records = []
    for _, row in df.iterrows():
        for r in rates:
            res = simulate_buy_vs_rent(row, years=10, mortgage_rate=r)
            stress_records.append({
                "City": row["City"],
                "Mortgage_Rate_%": round(r * 100, 1),
                "Buyer_Advantage_$": res["Diff"]
            })

    stress_df = pd.DataFrame(stress_records)
    pivot = stress_df.pivot(index="City", columns="Mortgage_Rate_%", values="Buyer_Advantage_$")

    print("\n=== STRESS TEST: BUYER NET WORTH MINUS RENTER NET WORTH ($) ===")
    print(pivot.to_string())

    fig, ax = plt.subplots(figsize=(9, 6))
    for city in pivot.index:
        ax.plot(pivot.columns, pivot.loc[city] / 1000, marker="o", label=city)

    ax.axhline(0, color="black", linestyle="--", label="Break-Even Line ($0)")
    ax.set_xlabel("Mortgage Interest Rate (%)")
    ax.set_ylabel("Buyer Advantage Over Renting ($ Thousands)")
    ax.set_title("10-Year Buy vs. Rent + Invest Stress Test Across Canada")
    ax.legend()

    plt.tight_layout()
    plt.savefig("charts/buy_vs_rent_stress.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    run_buy_vs_rent_stress_test()
