import numpy as np
import pandas as pd
from city_data import get_canadian_cities

def calculate_irr(cash_flows):
    
    roots = np.roots(cash_flows[::-1])
    real_roots = roots[np.isreal(roots)].real
    valid_roots = [r for r in real_roots if r > 0]
    if not valid_roots:
        return np.nan
    best_root = min(valid_roots, key=lambda r: abs(r - 1.0))
    return (1.0 / best_root) - 1.0

def simulate_pe_buyout(city_row, turnover_rate=0.10, reno_cost_per_unit=0,
                       ltv=0.70, interest_rate=0.050, market_rent_growth=0.03,
                       force_vacancy_control=False):
    """
   
    """
    units = city_row["Units"]
    purchase_price = city_row["Purchase_Price"]
    
    loan_amount = purchase_price * ltv
    initial_equity = purchase_price * (1 - ltv)
    annual_interest = loan_amount * interest_rate
    
    current_avg_rent = city_row["Occupied_Rent"]
    market_rent = city_row["Market_Rent"]
    rent_cap = city_row["Rent_Cap"]
    
    vacancy_decontrol = False if force_vacancy_control else city_row["Vacancy_Decontrol"]
    expense_ratio = city_row["Expense_Ratio"]
    
    cash_flows = [-initial_equity]  # Year 0 investment
    
    for year in range(1, 6):
        market_rent *= (1 + market_rent_growth)
        
        turned_units = units * turnover_rate
        stayed_units = units - turned_units
        
        effective_renewal_hike = min(rent_cap, market_rent_growth)
        stayed_rent = current_avg_rent * (1 + effective_renewal_hike)
        
        if vacancy_decontrol:
            turned_rent = market_rent
        else:
            turned_rent = current_avg_rent * (1 + rent_cap)
            
        current_avg_rent = ((stayed_units * stayed_rent) + (turned_units * turned_rent)) / units
        
        gross_rent = units * current_avg_rent * 12
        noi = gross_rent * (1 - expense_ratio)
        reno_capex = turned_units * reno_cost_per_unit
        net_cash_flow = noi - annual_interest - reno_capex
        
        if year == 5:
            entry_cap = city_row["Year1_NOI"] / purchase_price
            exit_cap = entry_cap + 0.0025  # Conservative 0.25% exit buffer
            exit_valuation = noi / exit_cap
            net_cash_flow += (exit_valuation - loan_amount)
            
        cash_flows.append(net_cash_flow)
        
    irr = calculate_irr(cash_flows) * 100
    rent_increase_pct = ((current_avg_rent - city_row["Occupied_Rent"]) / city_row["Occupied_Rent"]) * 100
    
    return {
        "City": city_row["City"],
        "Prov": city_row["Province"],
        "IRR_%": round(irr, 1),
        "5Yr_Rent_Hike_%": round(rent_increase_pct, 1),
        "End_Avg_Rent": round(current_avg_rent, 0),
        "Hits_15%_Hurdle": irr >= 15.0
    }

if __name__ == "__main__":
    df_cities = get_canadian_cities()
    
    print("\n=== 1. PASSIVE HOLD (10% Organic Turnover, $0 Reno) ===")
    s1 = [simulate_pe_buyout(row, turnover_rate=0.10, reno_cost_per_unit=0) for _, row in df_cities.iterrows()]
    print(pd.DataFrame(s1).to_string(index=False))
    
    print("\n=== 2. VALUE-ADD (30% Turnover, $20k/Unit Reno) ===")
    s2 = [simulate_pe_buyout(row, turnover_rate=0.30, reno_cost_per_unit=20000) for _, row in df_cities.iterrows()]
    print(pd.DataFrame(s2).to_string(index=False))

    print("\n=== 3. WHAT IF ALL PROVINCES BAN VACANCY DECONTROL? ===")
    s3 = [simulate_pe_buyout(row, turnover_rate=0.30, reno_cost_per_unit=20000, force_vacancy_control=True) for _, row in df_cities.iterrows()]
    print(pd.DataFrame(s3).to_string(index=False))
