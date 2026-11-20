import pandas as pd

def get_canadian_cities():

    cities = [
        {
            "City": "Toronto",
            "Province": "Ontario",
            "Units": 60,
            "Price_Per_Unit": 420000,
            "Occupied_Rent": 1950,          
            "Market_Rent": 2650,           
            "Rent_Cap": 0.021,             
            "Vacancy_Decontrol": True,     
            "Expense_Ratio": 0.38


        },
        {
            "City": "Vancouver",
            "Province": "British Columbia",
            "Units": 60,
            "Price_Per_Unit": 460000,
            "Occupied_Rent": 2100,          
            "Market_Rent": 2950,           
            "Rent_Cap": 0.023,             
            "Vacancy_Decontrol": True,     
            "Expense_Ratio": 0.36
        },
        {
            "City": "Montreal",
            "Province": "Quebec",
            "Units": 60,
            "Price_Per_Unit": 260000,
            "Occupied_Rent": 1450,          
            "Market_Rent": 1950,           
            "Rent_Cap": 0.031,             
            "Vacancy_Decontrol": False,     
            "Expense_Ratio": 0.42
        },
        {
            "City": "Halifax",
            "Province": "NS",
            "Units": 60,
            "Price_Per_Unit": 275000,
            "Occupied_Rent": 1650,
            "Market_Rent": 2200,
            "Rent_Cap": 0.050,              # Nova Scotia 5.0% temporary cap
            "Vacancy_Decontrol": True,
            "Expense_Ratio": 0.40
        },
        {
            "City": "Calgary",
            "Province": "AB",
            "Units": 60,
            "Price_Per_Unit": 285000,
            "Occupied_Rent": 1750,
            "Market_Rent": 1900,
            "Rent_Cap": 1.00,               # Alberta has no statutory percentage cap
            "Vacancy_Decontrol": True,
            "Expense_Ratio": 0.39
        },
        {
            "City": "Edmonton",
            "Province": "AB",
            "Units": 60,
            "Price_Per_Unit": 215000,
            "Occupied_Rent": 1400,
            "Market_Rent": 1525,
            "Rent_Cap": 1.00,               # Alberta has no statutory percentage cap
            "Vacancy_Decontrol": True,
            "Expense_Ratio": 0.43
        }
]

    df = pd.DataFrame(cities)

    df["Purchase_Price"] = df["Units"] * df["Price_Per_Unit"]
    df["Year1_NOI"] = (
        df["Units"] * df["Occupied_Rent"] * 12 * (1 - df["Expense_Ratio"])
    )
    df["Year1_NOI"] = df["Occupied_Rent"] * 12 * df["Units"] * (1 - df["Expense_Ratio"])
    df["Cap_Rate_%"] = round((df["Year1_NOI"] / df["Purchase_Price"]) * 100, 2)
    df["Rent_Gap_%"] = round(((df["Market_Rent"] - df["Occupied_Rent"]) / df["Occupied_Rent"]) * 100, 1)

    return df


if __name__ == "__main__":
    data = get_canadian_cities()
    print("\n--- CANADIAN 6-CITY PE HOUSING BASELINE ---")
    print(data[["City", "Province", "Purchase_Price", "Year1_NOI", "Cap_Rate_%", "Rent_Gap_%", "Vacancy_Decontrol"]].to_string(index=False))
           
    

