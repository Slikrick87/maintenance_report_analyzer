import pandas as pd

# Load your lookup table
cost_lookup = pd.read_csv("cost_lookup.csv")

def get_estimated_cost(description):
    for _, row in cost_lookup.iterrows():
        if row['Keyword'].lower() in description.lower():
            return row['Estimated Cost']
    return 25  # Default cost if no keyword matches

# Example usage:
desc = "Replaced Wiring Harness For Fuel Pump"
cost = get_estimated_cost(desc)
print(cost)  # Output: 150 (matches "Wiring Harness")